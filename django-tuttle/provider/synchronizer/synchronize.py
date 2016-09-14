import logging

from github import BadCredentialsException
from github import Github
from github import GithubException

from provider.models import Token, DeployKey, Repository

logger = logging.getLogger()


def synchronize(user):
    """
    sychronize function retrieve all the github user's repositories
    :param user:
    """
    try:
        # retrieve user's token
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        raise

    try:
        # login on github account using user's token
        logger.info('logging on github')
        login = Github(token.token)

    except BadCredentialsException:
        logger.error('Invalid credentials')
        raise BadCredentialsException('', '')

    current_user = login.get_user()

    # check token scopes
    scope_list = current_user.raw_headers['x-oauth-scopes']
    if 'repo' not in scope_list:
        logger.info('no "repo" attribute for the current token')
        raise GithubException('', '')
    # delete user's deploy keys
    DeployKey.objects.filter(repository__user=token.user).delete()
    # get repository info of the logged user
    for repo in current_user.get_repos():
        params = {
            'name': repo.name,
            'owner': repo.owner.login,
            'organization': getattr(repo.organization, 'name', None),
            'is_private': repo.private,
            'is_user_admin': repo.permissions.admin,
            'user': token.user,
            'provider': token.provider,
        }
        try:
            Repository.objects.get_or_create(**params)

        except Repository.MultipleObjectsReturned:
            msg = 'More than 1 Repository with this params: %s ' % params
            logger.error(msg)
            raise
        # user must be admin of his repository for get the deploy keys
        if repo.permissions.admin:
            for key in repo.get_keys():
                params = {
                    'title': key.title,
                    'key': key.key,
                    'repository': Repository.objects.get(name=repo.name),
                }
                DeployKey.objects.create(**params)
