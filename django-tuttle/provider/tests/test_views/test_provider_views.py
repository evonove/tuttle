import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from provider.models import Repository, Provider, DeployKey


@pytest.mark.django_db
def test_deplokey_list_view(client):
    user = get_user_model().objects.create(username='username', password='123456', email='test@test.it')
    provider = Provider.objects.create(name='github')
    repository = Repository.objects.create(name='test', owner='user', organization='', is_private=False, user=user,
                                           provider=provider)
    # Token.objects.create(title='test', token='123456', provider=provider, user=user)
    DeployKey.objects.create(title='key', key='123456', repository=repository)
    client.login(username='username', password='123456')
    response = client.get(reverse('deploykey_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_repository_list_view(client):
    user = get_user_model().objects.create(username='username', password='123456', email='test@test.it')
    provider = Provider.objects.create(name='github')
    Repository.objects.create(name='test', owner='user', organization='', is_private=False, user=user,
                              provider=provider)
    client.login(username='username', password='123456')
    response = client.get(reverse('repo_list'))
    assert response.status_code == 200
