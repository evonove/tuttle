import logging

from github import BadCredentialsException
from github import Github

from provider.models import Token, DeployKey, Repository

logger = logging.getLogger()


class Synchronize:

    def __init__(self, user):
        self.user = user

    def create_repository(self, **params):
        """
         Create repository object
        """
        try:
            Repository.objects.get_or_create(**params)
        except Repository.MultipleObjectsReturned:
            raise

    def create_deploykey(self, **params):
        """
        Create deploykey object
        """
        DeployKey.objects.create(**params)

    def delete_deploykeys(self, token):
        """
        Delete Deploykey objects of a specific user
        """
        DeployKey.objects.filter(repository__user=token.user).delete()

    def run(self):
        """
        Get all user's token
        """
        for token in Token.objects.filter(user=self.user):
            if token.provider.name == 'Github':
                g = GithubSyn(self.user, token)
                g.run()
            # elif token.provider.name == 'Bitbucket':


class GithubSyn(Synchronize):

    def __init__(self, user, token):
        self.token = token
        Synchronize.__init__(self, user)

    def login(self):
        """
        Login on github and check token's scope
        """
        try:
            login = Github(self.token.token)
            user = login.get_user()
        except BadCredentialsException:
            raise BadCredentialsException('', '')

        scope_list = user.raw_headers['x-oauth-scopes']
        if 'repo' not in scope_list:
            raise BadCredentialsException('', '')
        return user

    def get_repo(self):
        current_user = self.login()
        repo_list = []
        for repo in current_user.get_repos():
            repo_list.append(repo)
        return repo_list

    def get_repo_params(self):
        if self.get_repo():
            for repo in self.get_repo():
                params = {
                    'name': repo.name,
                    'owner': repo.owner.login,
                    'organization': getattr(repo.organization, 'name', None),
                    'is_private': repo.private,
                    'is_user_admin': repo.permissions.admin,
                    'user': self.user,
                    'provider': self.token.provider,
                }
                self.create_repository(**params)

    def get_deploykey(self):
        current_user = self.login()
        key_list = []
        repo_name = []
        for repo in current_user.get_repos():
            if repo.permissions.admin:
                for key in repo.get_keys():
                    key_list.append(key)
                    repo_name.append(repo.name)
                return key_list, repo_name

    def get_deploykey_params(self):
        self.delete_deploykeys(self.token)
        if self.get_deploykey():
            key_list, repo_list = self.get_deploykey()
            for key, repo in zip(key_list, repo_list):
                params = {
                    'title': key.title,
                    'key': key.key,
                    'repository': Repository.objects.get(name=repo),
                }
                self.create_deploykey(**params)

    def run(self):
        self.login()
        self.get_repo()
        self.get_deploykey()
        self.get_repo_params()
        self.get_deploykey_params()
