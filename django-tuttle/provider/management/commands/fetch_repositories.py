from django.core.management.base import BaseCommand, CommandError
from github import Github, BadCredentialsException
from tuttleuser.models import TuttleUser
from provider.models import Repository


class Command(BaseCommand):
    help = 'command for get repositories list from github account'

    def handle(self, *args, **options):
        tuttle = TuttleUser.objects.get(username='girbons')

        try:
            login = Github(tuttle.token)
            user = login.get_user()
            for repo in user.get_repos():
                Repository.objects.get_or_create(name=repo.name, user=tuttle)
        except BadCredentialsException:
            raise CommandError("can't login on github account")

