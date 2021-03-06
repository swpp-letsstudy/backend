from rest_framework.test import APITestCase
from django.contrib.auth.models import User


USERS_INFO = [{
    'username': 'user%d' % i,
    'password': '1234'
} for i in range(3)]


GROUPS_INFO = [{
    'name': 'group%d' % i,
    'info': 'info',
} for i in range(3)]


class GroupTestCase(APITestCase):

    def setUp(self):
        for USER_INFO in USERS_INFO:
            User.objects.create_user(**USER_INFO)
        self.token = None

    def login(self, user_info):
        response = self.client.post('/login/', user_info)
        self.token = response.data['token']
        return User.objects.get(auth_token=self.token)

    def header(self):
        return {'HTTP_AUTHORIZATION': 'Token %s' % self.token} if self.token else {}

    def get(self, path):
        return self.client.get(path, **self.header())

    def post(self, path, data):
        return self.client.post(path, data, **self.header())

    def test_create_group(self):
        self.login(USERS_INFO[0])

        for GROUP_INFO in GROUPS_INFO:
            response = self.post('/groups/', GROUP_INFO)
            self.assertEqual(response.status_code, 201)

        response = self.get('/groups/')
        self.assertEqual(response.status_code, 200)
        for i, GROUP_INFO in enumerate(GROUPS_INFO):
            for key_value in GROUP_INFO.items():
                self.assertIn(key_value, response.data[i].items())
