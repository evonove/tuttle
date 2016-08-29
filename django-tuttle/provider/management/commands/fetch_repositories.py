from django.core.management.base import BaseCommand, CommandError
from github import Github, BadCredentialsException
from tuttleuser.models import TuttleUser
from provider.models import Repository, Provider


class Command(BaseCommand):
    help = 'command for get repositories list from github account'

    def handle(self, *args, **options):
        tuttle = TuttleUser.objects.get(username='girbons')
        provider = Provider.objects.get(name='github')

        try:
            login = Github(tuttle.token)
            user = login.get_user()

            self.stdout.write('saving repository info')
            for repo in user.get_repos():
                if repo.organization is not None:
                    Repository.objects.get_or_create(name=repo.name, owner=repo.owner.login,
                                                     organization=repo.organization.name, is_private=repo.private,
                                                     user=tuttle, provider=provider)
                    self.stdout.write(repo.name)
                else:
                    Repository.objects.get_or_create(name=repo.name, owner=repo.owner.login, is_private=repo.private,
                                                     user=tuttle, provider=provider)
                    self.stdout.write(repo.name)
        except BadCredentialsException:
            raise CommandError("can't login on github account, invalid token")
