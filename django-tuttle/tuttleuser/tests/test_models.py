import pytest

from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestTuttleUser(object):
    """
    tests tuttle user
    """
    def test_users_get_full_name(self):
        user = get_user_model().objects.create(username='user', email='test@test.it', first_name='name',
                                               last_name='last name')
        assert user.get_full_name() == 'name last name'

    def test_user_token_exist(self):
        user = get_user_model().objects.create(username='user', email='test@test.it', first_name='name',
                                               last_name='last name', token='123456')
        assert user.token == '123456'
