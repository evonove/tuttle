import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from provider.synchronizer.github import synchronize_github

logger = logging.getLogger()


class Command(BaseCommand):
    help = 'command for get repositories list from github account'

    def add_arguments(self, parser):
        # arguments required for launch the command
        parser.add_argument('-u', '--user', dest='user', required=True)

    def handle(self, *args, **options):
        user_argument = options['user']
        try:
            user = get_user_model().objects.get(username=user_argument)
        except get_user_model().DoesNotExist:
            raise CommandError('User object doesn\'t exist')
        synchronize_github(user)
