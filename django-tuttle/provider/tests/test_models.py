import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from ..models import Provider, Repository, DeployKey


@pytest.mark.django_db
class TestProvider(object):
    """
    tests for provider model
    """

    def test_provider_name(self):
        Provider.objects.create(name='github')
        assert Provider.objects.count() == 1

    def test_provider_representation(self):
        provider = Provider.objects.create(name='github')
        assert '%s' % provider


@pytest.mark.django_db
class TestRepository(object):
    """
    tests for repository model
    """

    def test_repository_create(self):
        user = get_user_model().objects.create(username='provola', email='test@gmail.com', first_name='name',
                                               last_name='surname')
        Repository.objects.create(name='prova', user=user)
        assert Repository.objects.count() == 1

    def test_repository_with_no_user(self):
        with pytest.raises(IntegrityError):
            Repository.objects.create(name='prova')


@pytest.mark.django_db
class TestDeployKey(object):
    """
    test for deploykey model
    """

    def test_deploykey_create(self):
        user = get_user_model().objects.create(username='provola', email='test@gmail.com', first_name='name',
                                               last_name='surname')
        repo = Repository.objects.create(name='test', user=user)
        DeployKey.objects.create(title='pippo', key='123456', repository=repo)

    def test_deploykey_without_user(self):
        with pytest.raises(IntegrityError):
            DeployKey.objects.create(title='pippo', key='1245')
