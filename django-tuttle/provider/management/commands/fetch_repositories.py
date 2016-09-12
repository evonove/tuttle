import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from github import Github, BadCredentialsException
from provider.models import Repository, Provider, DeployKey, Token

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
            # getting token and provider objects
            token = Token.objects.get(token=token_argument)
            provider = Provider.objects.get(name=provider_argument)

        except Token.DoesNotExist:
            logger.error('Token objects doesn\'t exist')
            raise CommandError('Token object doesn\'t exist')

        except Provider.DoesNotExist:
            logger.error('Provider objects doesn\'t exist')
            raise CommandError('Provider object doesn\'t exist')

        try:
            # login on github account using user's token
            login = Github(token.token)
            user = login.get_user()

            # check token scopes
            scope_list = user.raw_headers['x-oauth-scopes']
            if 'repo' in scope_list:
                self.stdout.write('Saving repository info')
                # delete user's deploy keys
                DeployKey.objects.filter(repository__user=token.user).delete()
                # get repository info of the logged user
                for repo in user.get_repos():
                    params = {
                        'name': repo.name,
                        'owner': repo.owner.login,
                        'organization': getattr(repo.organization, 'name', None),
                        'is_private': repo.private,
                        'is_user_admin': repo.permissions.admin,
                        'user': token.user,
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
                            try:
                                DeployKey.objects.create(**params)

                            except IntegrityError:
                                msg = 'Error during the object creation'
                                logger.error(msg)
                                raise CommandError(msg)

            else:
                raise CommandError('Your token has not REPO scope')

        except BadCredentialsException:
            logger.error('Login error on %s' % provider)
            raise CommandError('Can\'t login on github account, invalid token')
