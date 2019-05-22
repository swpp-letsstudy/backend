from rest_framework.test import APITestCase
from django.contrib.auth.models import User


USERS_INFO = [{
    'username': 'user{}'.format(i),
    'password': '1234'
} for i in range(3)]


class UserTestCase(APITestCase):
    def setUp(self):
        for USER_INFO in USERS_INFO:
            User.objects.create_user(**USER_INFO)

    def test_login(self):
        for USER_INFO in USERS_INFO:
            response = self.client.post('/login/', USER_INFO)
            self.assertEqual(response.status_code, 200)
