import pytest

from django.contrib.auth import get_user_model
from django.core.management import CommandError
from django.core.management import call_command
from django.db import IntegrityError
from github import BadCredentialsException
from github.Repository import Repository as GithubRepo
from provider.models import Provider, Repository, DeployKey, Token
from unittest.mock import MagicMock, patch


@pytest.mark.django_db
def test_fetch_repositories_with_organization_field():
    """
    Test the correct creation of Repository object with organization field
    """
    with patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization.name = 'test-organization'
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False
        github_repo_mock.permissions.admin = True

        # mock get_repos() method
        githubMock = githubMock.return_value
        githubMock.get_user = MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = MagicMock(return_value=[github_repo_mock])

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of objects User, Provider, Token
        user = get_user_model().objects.create(username='username', email='test@test.it')
        provider = Provider.objects.create(name=provider_arg)
        Token.objects.create(title='test', token=token_arg, provider=provider, user=user)
        call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        assert Repository.objects.count() == 1


@pytest.mark.django_db
def test_fetch_repositories_with_empty_organization_field():
    """
    Test the correct creation of Repository object with empty organization field
    """
    with patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization = None
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False
        github_repo_mock.permissions.admin = True

        # mock get_repos() method
        githubMock = githubMock.return_value
        githubMock.get_user = MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = MagicMock(return_value=[github_repo_mock])

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of object User, Provider, Token
        user = get_user_model().objects.create(username='username', email='test@test.it')
        provider = Provider.objects.create(name=provider_arg)
        Token.objects.create(title='test', token=token_arg, provider=provider, user=user)

        call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        repository = Repository.objects.get(name='test')

        assert Repository.objects.count() == 1
        assert repository.organization is None


@pytest.mark.django_db
def test_fetch_repositories_get_deploykey():
    """
    Test the correct creation of Deploy key object
    """
    with patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization = None
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False
        github_repo_mock.permissions.admin = True

        # mock methods
        githubMock = githubMock.return_value
        githubMock.get_user = MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = MagicMock(return_value=[github_repo_mock])
        github_repo_mock.get_keys = MagicMock(return_value=[github_repo_mock])

        # assignment parameters for create deploy key object
        github_repo_mock.permissions.admin = True
        github_repo_mock.title = 'test key'
        github_repo_mock.key = '123456'

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of objects TuttleUser and Provider
        user = get_user_model().objects.create(username='username', email='test@test.it')
        provider = Provider.objects.create(name=provider_arg)
        Token.objects.create(title='test', token=token_arg, provider=provider, user=user)
        call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        key = DeployKey.objects.get(title='test key')
        assert DeployKey.objects.count() == 1
        assert key.title == 'test key'
        assert key.key == '123456'


@pytest.mark.django_db
def test_fetch_repositories_with_no_provider_object():
    """
    Test error while launching fetch_repositories command without required argument
    """
    # creation of arguments needed for execute the django command
    token_arg = '123456'

    # creation of object User, Provider, Token
    user = get_user_model().objects.create(username='username', email='test@test.it')
    provider = Provider.objects.create(name='test')
    Token.objects.create(title='test', token=token_arg, provider=provider, user=user)

    with pytest.raises(CommandError) as ex:
        call_command('fetch_repositories', '-t', token_arg)
    assert 'Error: the following arguments are required: -p/--provider' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_with_no_token_object():
    """
   Test error while launching fetch_repositories command without required argument
   """
    # creation of arguments needed for execute the django command
    provider_arg = 'test'

    # creation of object Provider
    Provider.objects.create(name=provider_arg)

    with pytest.raises(CommandError) as ex:
        call_command('fetch_repositories', '-p', provider_arg)
    assert 'Error: the following arguments are required: -t/--token' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_with_no_args():
    """
    Test error while launching fetch_repositories command without required arguments
    """
    with pytest.raises(CommandError) as ex:
        call_command('fetch_repositories')
    assert 'Error: the following arguments are required: -t/--token, -p/--provider' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_provider_does_not_exist():
    """
    Test error while launching fetch_repositories command with argument that doesn't exist
    """
    # creation of arguments needed for execute the django command
    token_arg = '123456'

    # creation of object User, Provider, Token
    user = get_user_model().objects.create(username='username', email='test@test.it')
    provider = Provider.objects.create(name='test')
    Token.objects.create(title='test', token=token_arg, provider=provider, user=user)

    with pytest.raises(CommandError) as ex:
        call_command('fetch_repositories', '-t', token_arg, '-p', 'provider test')
    assert 'Provider object doesn\'t exist' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_token_does_not_exist():
    """
    Test error while launching fetch_repositories command with argument that doesn't exist
    """
    # creation of arguments needed for execute the django command
    provider_arg = 'test'

    # creation of object Provider
    Provider.objects.create(name=provider_arg)
    with pytest.raises(CommandError) as ex:
        call_command('fetch_repositories', '-t', '11111', '-p', provider_arg)
    assert 'Token object doesn\'t exist' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_with_invalid_token():
    """
    Test error login
    """
    with patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        githubMock.side_effect = BadCredentialsException(status='', data='')
        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of object User, Provider, Token
        user = get_user_model().objects.create(username='username', email='test@test.it')
        provider = Provider.objects.create(name=provider_arg)
        Token.objects.create(title='test', token=token_arg, provider=provider, user=user)

        with pytest.raises(CommandError) as ex:
            call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        assert 'Can\'t login on github account, invalid token' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_organization_multiple_objects_returned():
    with patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization.name = 'test organization'
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False
        github_repo_mock.permissions.admin = True

        # mock get_repos() method
        githubMock = githubMock.return_value
        githubMock.get_user = MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = MagicMock(return_value=[github_repo_mock])

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of object User, Provider, Token
        user = get_user_model().objects.create(username='username', email='test@test.it')
        provider = Provider.objects.create(name=provider_arg)
        Token.objects.create(title='test', token=token_arg, provider=provider, user=user)

        Repository.objects.create(name='test', owner='user test', organization='test organization',
                                  is_private=False, is_user_admin=True, user=user, provider=provider)

        Repository.objects.create(name='test', owner='user test', organization='test organization',
                                  is_private=False, is_user_admin=True, user=user, provider=provider)

        with pytest.raises(CommandError) as ex:
            call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        assert 'Fix the database' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_without_organization_multiple_objects_returned():
    with patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization = None
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False
        github_repo_mock.permissions.admin = True

        # mock get_repos() method
        githubMock = githubMock.return_value
        githubMock.get_user = MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = MagicMock(return_value=[github_repo_mock])

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of object User, Provider, Token
        user = get_user_model().objects.create(username='username', email='test@test.it')
        provider = Provider.objects.create(name=provider_arg)
        Token.objects.create(title='test', token=token_arg, provider=provider, user=user)

        Repository.objects.create(name='test', owner='user test', is_private=False, is_user_admin=True,
                                  user=user, provider=provider)

        Repository.objects.create(name='test', owner='user test', is_private=False, is_user_admin=True,
                                  user=user, provider=provider)

        with pytest.raises(CommandError) as ex:
            call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        assert 'Fix the database' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_deploy_keys_exception():
    with patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization = None
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False
        github_repo_mock.permissions.admin = True

        # mock methods
        githubMock = githubMock.return_value
        githubMock.get_user = MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = MagicMock(return_value=[github_repo_mock])
        github_repo_mock.get_keys = MagicMock(return_value=[github_repo_mock])

        # assignment parameters for create deploy key object
        github_repo_mock.permissions.admin = True
        github_repo_mock.title = 'test key'
        github_repo_mock.key = '123456'

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of object User, Provider, Token
        user = get_user_model().objects.create(username='username', email='test@test.it')
        provider = Provider.objects.create(name=provider_arg)
        Token.objects.create(title='test', token=token_arg, provider=provider, user=user)

        Repository.objects.create(name='test', owner='user test', is_private=False,
                                  is_user_admin=True, user=user, provider=provider)
        with pytest.raises(IntegrityError) as ex:
            DeployKey.objects.create(title='test key', key='123456')
            call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        assert ex.match(r'.*null value in column "repository_id"')
