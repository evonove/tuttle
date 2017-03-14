import logging

from django.core.management.base import BaseCommand, CommandError

from provider.models import Token
from provider.synchronizer.synchronize import Synchronize


logger = logging.getLogger()


class Command(BaseCommand):
    help = 'command for get repositories list from github account'

    def add_arguments(self, parser):
        # arguments required for launch the command
        parser.add_argument('-u', '--user', dest='user', required=True)

    def handle(self, *args, **options):
        user_argument = options['user']
        try:
            token = Token.objects.get(user__username=user_argument)
        except Token.DoesNotExist:
            raise CommandError('User does not have a token key')
        Synchronize(token).run()
