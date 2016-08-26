import pytest

from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestTuttleUser(object):
    """
    tests tuttle user
    """
    def test_users_get_full_name(self):
        user = get_user_model().objects.create(username='provola', email='test@test.it', first_name='aldo',
                                               last_name='bi')
        assert user.get_full_name() == 'aldo bi'

    def test_user_token_exist(self):
        user = get_user_model().objects.create(username='provola', email='test@test.it', first_name='aldo',
                                               last_name='bi', token='123456')
        assert user.token == '123456'
