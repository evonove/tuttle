import pytest
import mock

from django.contrib.auth import get_user_model
from django.core.management import CommandError
from django.core.management import call_command
from github import BadCredentialsException
from github.Repository import Repository as GithubRepo
from provider.models import Provider, Repository, DeployKey


@pytest.mark.django_db
def test_fetch_repositories_with_organization_field():
    """
    Test the correct creation of Repository object with organization field
    """
    with mock.patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = mock.MagicMock()
        github_repo_mock = mock.MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization.name = 'test-organization'
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False

        # mock get_repos() method
        githubMock = githubMock.return_value
        githubMock.get_user = mock.MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = mock.MagicMock(return_value=[github_repo_mock])

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of objects TuttleUser and Provider
        get_user_model().objects.create(username='username', email='test@test.it', token=token_arg)
        Provider.objects.create(name=provider_arg)
        call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        assert Repository.objects.count() == 1


@pytest.mark.django_db
def test_fetch_repositories_with_empty_organization_field():
    """
    Test the correct creation of Repository object with empty organization field
    """
    with mock.patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = mock.MagicMock()
        github_repo_mock = mock.MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization = None
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False

        # mock get_repos() method
        githubMock = githubMock.return_value
        githubMock.get_user = mock.MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = mock.MagicMock(return_value=[github_repo_mock])

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of objects TuttleUser and Provider
        get_user_model().objects.create(username='username', email='test@test.it', token=token_arg)
        Provider.objects.create(name=provider_arg)

        call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        repository = Repository.objects.get(name='test')

        assert Repository.objects.count() == 1
        assert repository.organization is None


@pytest.mark.django_db
def test_fetch_repositories_get_deploykey():
    """
    Test the correct creation of Deploy key object
    """
    with mock.patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = mock.MagicMock()
        github_repo_mock = mock.MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization = None
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False

        # mock methods
        githubMock = githubMock.return_value
        githubMock.get_user = mock.MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = mock.MagicMock(return_value=[github_repo_mock])
        github_repo_mock.get_keys = mock.MagicMock(return_value=[github_repo_mock])

        # assignment parameters for create deploy key object
        github_repo_mock.permissions.admin = True
        github_repo_mock.title = 'test key'
        github_repo_mock.key = '123456'

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of objects TuttleUser and Provider
        get_user_model().objects.create(username='username', email='test@test.it', token=token_arg)
        Provider.objects.create(name=provider_arg)
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

    # creation of object TuttleUser
    get_user_model().objects.create(username='username', email='test@test.it', token=token_arg)

    with pytest.raises(CommandError) as ex:
        call_command('fetch_repositories', '-t', token_arg)
    assert 'Error: the following arguments are required: -p/--provider' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_with_no_user_object():
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

    # creation of object TuttleUser
    get_user_model().objects.create(username='username', email='test@test.it', token=token_arg)

    with pytest.raises(CommandError) as ex:
        call_command('fetch_repositories', '-t', token_arg, '-p', 'provider test')
    assert 'Provider object doesn\'t exist' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_user_does_not_exist():
    """
    Test error while launching fetch_repositories command with argument that doesn't exist
    """
    # creation of arguments needed for execute the django command
    provider_arg = 'test'

    # creation of object Provider
    Provider.objects.create(name=provider_arg)

    with pytest.raises(CommandError) as ex:
        call_command('fetch_repositories', '-t', '11111', '-p', provider_arg)
    assert 'User object doesn\'t exist' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_with_invalid_token():
    """
    Test error login
    """
    with mock.patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        githubMock.side_effect = BadCredentialsException(status='', data='')
        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of objects TuttleUser and Provider
        get_user_model().objects.create(username='username', email='test@test.it', token=token_arg)
        Provider.objects.create(name=provider_arg)

        with pytest.raises(CommandError) as ex:
            call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        assert 'Can\'t login on github account, invalid token' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_organization_multiple_objects_returned():
    with mock.patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = mock.MagicMock()
        github_repo_mock = mock.MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization.name = 'test organization'
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False

        # mock get_repos() method
        githubMock = githubMock.return_value
        githubMock.get_user = mock.MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = mock.MagicMock(return_value=[github_repo_mock])

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of objects TuttleUser and Provider
        user = get_user_model().objects.create(username='username', email='test@test.it', token=token_arg)
        provider = Provider.objects.create(name=provider_arg)

        Repository.objects.create(name='test', owner='user test', organization='test organization',
                                  is_private=False, user=user, provider=provider)

        Repository.objects.create(name='test', owner='user test', organization='test organization',
                                  is_private=False, user=user, provider=provider)

        with pytest.raises(CommandError) as ex:
            call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        assert 'Fix the database' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_without_organization_multiple_objects_returned():
    with mock.patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = mock.MagicMock()
        github_repo_mock = mock.MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization = None
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False

        # mock get_repos() method
        githubMock = githubMock.return_value
        githubMock.get_user = mock.MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = mock.MagicMock(return_value=[github_repo_mock])

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of objects TuttleUser and Provider
        user = get_user_model().objects.create(username='username', email='test@test.it', token=token_arg)
        provider = Provider.objects.create(name=provider_arg)

        Repository.objects.create(name='test', owner='user test', is_private=False, user=user, provider=provider)

        Repository.objects.create(name='test', owner='user test', is_private=False, user=user, provider=provider)

        with pytest.raises(CommandError) as ex:
            call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        assert 'Fix the database' in str(ex.value)


@pytest.mark.django_db
def test_fetch_repositories_get_deploykey_multiple_objects_returned():
    with mock.patch('provider.management.commands.fetch_repositories.Github') as githubMock:
        github_user_mock = mock.MagicMock()
        github_repo_mock = mock.MagicMock(GithubRepo)

        # assignment parameters for the creation of Repository object
        github_repo_mock.name = 'test'
        github_repo_mock.organization = None
        github_repo_mock.owner.login = 'user test'
        github_repo_mock.private = False

        # mock methods
        githubMock = githubMock.return_value
        githubMock.get_user = mock.MagicMock(return_value=github_user_mock)
        github_user_mock.get_repos = mock.MagicMock(return_value=[github_repo_mock])
        github_repo_mock.get_keys = mock.MagicMock(return_value=[github_repo_mock])

        # assignment parameters for create deploy key object
        github_repo_mock.permissions.admin = True
        github_repo_mock.title = 'test key'
        github_repo_mock.key = '123456'

        # creation of arguments needed for execute the django command
        token_arg = '123456'
        provider_arg = 'test'

        # creation of objects TuttleUser and Provider
        user = get_user_model().objects.create(username='username', email='test@test.it', token=token_arg)
        provider = Provider.objects.create(name=provider_arg)

        repository = Repository.objects.create(name='test', owner='user test', is_private=False,
                                               user=user, provider=provider)
        DeployKey.objects.create(title='test key', key='123456', repository=repository)
        DeployKey.objects.create(title='test key', key='123456', repository=repository)

        with pytest.raises(CommandError) as ex:
            call_command('fetch_repositories', '-t', token_arg, '-p', provider_arg)
        assert 'Fix the database' in str(ex.value)
