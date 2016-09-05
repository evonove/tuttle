import logging

from django.core.management.base import BaseCommand, CommandError
from github import Github, BadCredentialsException
from tuttleuser.models import TuttleUser
from provider.models import Repository, Provider, DeployKey

logger = logging.getLogger()


class Command(BaseCommand):
    help = 'command for get repositories list from github account'

    def add_arguments(self, parser):
        # arguments required for launch the command
        parser.add_argument('-t', '--token', dest='token', help='User token for provider', required=True)
        parser.add_argument('-p', '--provider', dest='provider', help='Provider\'s name', required=True)

    def handle(self, *args, **options):
        token_argument = options['token']
        provider_argument = options['provider']

        try:
            # getting user and provider objects
            tuttle = TuttleUser.objects.get(token=token_argument)
            provider = Provider.objects.get(name=provider_argument)

        except TuttleUser.DoesNotExist:
            logger.error('User objects doesn\'t exist')
            raise CommandError('User object doesn\'t exist')

        except Provider.DoesNotExist:
            logger.error('Provider objects doesn\'t exist')
            raise CommandError('Provider object doesn\'t exist')

        try:
            # login on github account using user's token
            login = Github(tuttle.token)
            user = login.get_user()
            self.stdout.write('Saving repository info')

            # get repository info of the logged user
            for repo in user.get_repos():
                params = {
                    'name': repo.name,
                    'owner': repo.owner.login,
                    'organization': getattr(repo.organization, 'name', None),
                    'is_private': repo.private,
                    'user': tuttle,
                    'provider': provider,
                }
                try:
                    Repository.objects.get_or_create(**params)
                    self.stdout.write(repo.name)

                except Repository.MultipleObjectsReturned:
                    msg = 'More than 1 Repository with this params: %s ' % params
                    logger.error(msg)
                    raise CommandError(msg, 'Fix the database')

                # user must be admin of his repository for get the deploy keys
                if repo.permissions.admin:
                    for key in repo.get_keys():
                        params = {
                            'title': key.title,
                            'key': key.key,
                            'repository': Repository.objects.get(name=repo.name),
                        }
                        # if key is not null, DeployKey object can be created using the previous params
                        if key:
                            try:
                                DeployKey.objects.get_or_create(**params)

                            except DeployKey.MultipleObjectsReturned:
                                msg = 'More than 1 Deploykey with this params: %s ' % params
                                logger.error(msg)
                                raise CommandError(msg, 'Fix the database')

        except BadCredentialsException:
            logger.error('Login error on %s' % provider)
            raise CommandError('Can\'t login on github account, invalid token')
