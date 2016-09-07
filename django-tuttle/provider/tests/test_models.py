import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from ..models import Provider, Repository, DeployKey, Token


@pytest.mark.django_db
class TestProvider(object):
    """
    Tests for provider model
    """

    def test_provider_name(self):
        Provider.objects.create(name='github')
        assert Provider.objects.count() == 1

    def test_provider_representation(self):
        provider = Provider.objects.create(name='github')
        assert provider.name == 'github'


@pytest.mark.django_db
class TestRepository(object):
    """
    Tests for repository model
    """

    def test_repository_create(self):
        user = get_user_model().objects.create(username='user', email='test@test.com', first_name='name',
                                               last_name='surname')
        provider = Provider.objects.create(name='github')
        Repository.objects.create(name='repository test', owner='user test', organization='organization',
                                  is_private=True, user=user, provider=provider)
        assert Repository.objects.count() == 1

    def test_repository_with_no_user(self):
        with pytest.raises(IntegrityError):
            provider = Provider.objects.create(name='github')
            Repository.objects.create(name='repository test', owner='user test', organization='organization',
                                      is_private=True, provider=provider)

    def test_repository_with_no_provider(self):
        with pytest.raises(IntegrityError):
            user = get_user_model().objects.create(username='user', email='test@test.com', first_name='name',
                                                   last_name='surname')
            Repository.objects.create(name='repository test', owner='user test', organization='organization',
                                      is_private=True, user=user)

    def test_repository_organization(self):
        user = get_user_model().objects.create(username='user', email='test@test.com', first_name='name',
                                               last_name='surname')
        provider = Provider.objects.create(name='github')
        repo = Repository.objects.create(name='repository test', owner='user test', organization='organization',
                                         is_private=True, user=user, provider=provider)
        assert repo.organization == 'organization'


@pytest.mark.django_db
class TestDeployKey(object):
    """
    Tests for deploykey model
    """

    def test_deploykey_create(self):
        user = get_user_model().objects.create(username='user', email='test@test.com', first_name='name',
                                               last_name='surname')
        provider = Provider.objects.create(name='github')
        repo = Repository.objects.create(name='repository test', owner='user test', organization='organization',
                                         is_private=True, user=user, provider=provider)
        DeployKey.objects.create(title='deploy key', key='123456', repository=repo)

    def test_deploykey_without_user(self):
        with pytest.raises(IntegrityError):
            DeployKey.objects.create(title='deploy key', key='1245')


@pytest.mark.django_db
class TestToken(object):
    """
    Tests for Token model
    """
    def test_token_create(self):
        user = get_user_model().objects.create(username='user', email='test@test.com', first_name='name',
                                               last_name='surname')
        provider = Provider.objects.create(name='github')
        Token.objects.create(title='test', token='123456', provider=provider, user=user)
        assert Token.objects.count() == 1

    def test_token_without_provider(self):
        user = get_user_model().objects.create(username='user', email='test@test.com', first_name='name',
                                               last_name='surname')
        with pytest.raises(IntegrityError):
            Token.objects.create(title='test', token='123456', user=user)

    def test_token_without_user(self):
        provider = Provider.objects.create(name='github')

        with pytest.raises(IntegrityError):
            Token.objects.create(title='test', token='123456', provider=provider)
