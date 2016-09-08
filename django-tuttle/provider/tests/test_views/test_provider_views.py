import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from provider.models import Repository, Provider, DeployKey


@pytest.mark.django_db
def test_repository_list_view_without_login(client):
    response = client.get(reverse('repo_list'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_deploykey_list_view_without_login(client):
    response = client.get(reverse('deploykey_list'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_repository_list_view(client):
    get_user_model().objects.create_user(username='username', email='test@test.it', password='123456')
    # client.post('/accounts/login/', {'username': 'username', 'password': '123456'})
    client.login(username='username', password='123456')
    response = client.get(reverse('repo_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_deploykey_list_view(client):
    get_user_model().objects.create_user(username='username', email='test@test.it', password='123456')
    client.login(username='username', password='123456')
    response = client.get(reverse('deploykey_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_repository_list_view_contain_repo(client):
    provider = Provider.objects.create(name='test')
    user = get_user_model().objects.create_user(username='username', email='test@test.it', password='123456')
    Repository.objects.create(name='test', owner='user', organization='organization', is_private=False,
                              is_user_admin=True, user=user, provider=provider)
    client.login(username='username', password='123456')
    response = client.get(reverse('repo_list'))
    assert '<p>test</p>' in response.rendered_content


@pytest.mark.django_db
def test_deploykey_list_view_contain_key(client):
    provider = Provider.objects.create(name='test')
    user = get_user_model().objects.create_user(username='username', email='test@test.it', password='123456')
    repository = Repository.objects.create(name='test', owner='user', organization='organization', is_private=False,
                                           is_user_admin=True, user=user, provider=provider)
    DeployKey.objects.create(title='test key', key='123456', repository=repository)
    client.login(username='username', password='123456')
    response = client.get(reverse('deploykey_list'))
    assert '<p>test</p>' in response.rendered_content
    assert '<input type="text" value="123456" readonly>' in response.rendered_content
