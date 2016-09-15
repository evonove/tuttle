import pytest

from django.contrib.auth import get_user_model
from django.core.management import CommandError
from django.core.management import call_command
from github import BadCredentialsException
from github import GithubException
from github.Repository import Repository as GithubRepo
from provider.models import Provider, Repository, DeployKey, Token
from unittest.mock import MagicMock, patch


@pytest.mark.django_db
def test_fetch_repositories_with_organization_field():
    """
    Test the correct creation of Repository object with organization field
    """
    with patch('provider.synchronizer.synchronize.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignement scope to user's token
        github_user_mock.raw_headers = {'x-oauth-scopes': 'repo'}

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
        call_command('fetch_repositories', '-u', user)
        assert Repository.objects.count() == 1


@pytest.mark.django_db
def test_fetch_repositories_with_empty_organization_field():
    """
    Test the correct creation of Repository object with empty organization field
    """
    with patch('provider.synchronizer.synchronize.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignement scope to user's token
        github_user_mock.raw_headers = {'x-oauth-scopes': 'repo'}

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

        call_command('fetch_repositories', '-u', user)
        repository = Repository.objects.get(name='test')

        assert Repository.objects.count() == 1
        assert repository.organization is None


@pytest.mark.django_db
def test_fetch_repositories_get_deploykey():
    """
    Test the correct creation of Deploy key object
    """
    with patch('provider.synchronizer.synchronize.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignement scope to user's token
        github_user_mock.raw_headers = {'x-oauth-scopes': 'repo'}

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
        call_command('fetch_repositories', '-u', user)
        key = DeployKey.objects.get(title='test key')
        assert DeployKey.objects.count() == 1
        assert key.title == 'test key'
        assert key.key == '123456'


@pytest.mark.django_db
def test_fetch_repositories_with_no_user_object():
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
        call_command('fetch_repositories')
    assert 'Error: the following arguments are required: -u/--user' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_user_does_not_exist():
    """
    Test error while launching fetch_repositories command with argument that doesn't exist
    """
    with pytest.raises(CommandError) as ex:
        call_command('fetch_repositories', '-u', 'test')
    assert 'User object doesn\'t exist' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_with_invalid_token():
    """
    Test error login
    """
    with patch('provider.synchronizer.synchronize.Github') as githubMock:
        githubMock.side_effect = BadCredentialsException(status='', data='')
        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of object User, Provider, Token
        user = get_user_model().objects.create(username='username', email='test@test.it')
        provider = Provider.objects.create(name=provider_arg)
        Token.objects.create(title='test', token=token_arg, provider=provider, user=user)
        with pytest.raises(BadCredentialsException):
            call_command('fetch_repositories', '-u', user)


@pytest.mark.django_db
def test_fetch_repositories_organization_multiple_objects_returned():
    """
    Test MultipleObjectsException for get_or_create method
    :return:
    """
    with patch('provider.synchronizer.synchronize.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignement scope to user's token
        github_user_mock.raw_headers = {'x-oauth-scopes': 'repo'}

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

        with pytest.raises(Repository.MultipleObjectsReturned) as ex:
            call_command('fetch_repositories', '-u', user)
        assert 'get() returned more than one Repository -- it returned 2!' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_without_organization_multiple_objects_returned():
    """
    Test MultipleObjectsException for get_or_create method
    :return:
    """
    with patch('provider.synchronizer.synchronize.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignement scope to user's token
        github_user_mock.raw_headers = {'x-oauth-scopes': 'repo'}

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

        with pytest.raises(Repository.MultipleObjectsReturned) as ex:
            call_command('fetch_repositories', '-u', user)
        assert 'get() returned more than one Repository -- it returned 2!' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_token_no_scope():
    """
    Test GithubException with token that doesn't have the 'repo' scope
    :return:
    """
    with patch('provider.synchronizer.synchronize.Github') as githubMock:
        github_user_mock = MagicMock()
        github_repo_mock = MagicMock(GithubRepo)

        # assignement scope to user's token
        github_user_mock.raw_headers = {'x-oauth-scopes': ''}

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
        with pytest.raises(GithubException):
            call_command('fetch_repositories', '-u', user)


@pytest.mark.django_db
def test_fetch_repositories_token_does_not_exist():
    """
    test user's token doesn't exist
    :return:
    """
    user = get_user_model().objects.create(username='username', email='test@test.it')
    with pytest.raises(Token.DoesNotExist) as ex:
        call_command('fetch_repositories', '-u', user)
    assert 'Token matching query does not exist.' in str(ex.value)
