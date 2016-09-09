import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
def test_login_view(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_view(client):
    response = client.get(reverse('logout'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_view_without_login(client):
    response = client.get(reverse('profile'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_profile_view(client):
    get_user_model().objects.create_user(username='username', email='test@test.it', password='123456')
    client.login(username='username', password='123456')
    response = client.get(reverse('profile'))
    assert response.status_code == 200
    assert '<p>username</p>' in response.rendered_content
