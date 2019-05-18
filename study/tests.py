# from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from datetime import datetime, timezone

from study.models import StudyGroup


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


GROUPS_INFO = [{
    'name': 'group{}'.format(i),
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
        return {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)} if self.token else {}

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


MEETINGS_INFO = [{
    'time': datetime.now(timezone.utc).replace(
        minute=0, second=0, microsecond=0),
    'info': 'info',
}for i in range(3)]


class MeetingTestCase(APITestCase):

    def setUp(self):
        for USER_INFO in USERS_INFO:
            User.objects.create_user(**USER_INFO)
        self.token = None

    def login(self, user_info):
        response = self.client.post('/login/', user_info)
        self.token = response.data['token']
        return User.objects.get(auth_token=self.token)

    def header(self):
        return {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)} if self.token else {}

    def get(self, path):
        return self.client.get(path, **self.header())

    def post(self, path, data):
        return self.client.post(path, data, **self.header())
    
    def create_group(self, group_info):
        self.post('/groups/', group_info)
        return self.get('/groups/')
    
    def test_create_meeting(self):
        self.login(USERS_INFO[0])
        for GROUP_INFO in GROUPS_INFO:
            self.create_group(GROUP_INFO)

        group_id = StudyGroup.objects.all()[0].id

        for MEETING_INFO in MEETINGS_INFO:
            data = dict(list(MEETING_INFO.items()) + [('groupId',group_id)])
            response = self.post('/meetings/', data)
            self.assertEqual(response.status_code, 201)

        response = self.get('/meetings/?groupId={}'.format(group_id))
        self.assertEqual(response.status_code, 200)


class AttendanceTest(APITestCase):

    def setUp(self):
        for USER_INFO in USERS_INFO:
            User.objects.create_user(**USER_INFO)
        self.token = None
        self.create_meeting()

    def login(self, user_info):
        response = self.client.post('/login/', user_info)
        self.token = response.data['token']
        return User.objects.get(auth_token=self.token)

    def header(self):
        return {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)} if self.token else {}

    def get(self, path):
        return self.client.get(path, **self.header())

    def post(self, path, data):
        return self.client.post(path, data, **self.header())
    
    def put(self, path):
        return self.client.put(path, **self.header())

    def create_group(self, group_info):
        self.post('/groups/', group_info)
        return self.get('/groups/')
    
    def create_meeting(self):
        self.login(USERS_INFO[0])
        for GROUP_INFO in GROUPS_INFO:
            self.create_group(GROUP_INFO)

        group_id = StudyGroup.objects.all()[0].id

        for MEETING_INFO in MEETINGS_INFO:
            data = dict(list(MEETING_INFO.items()) + [('groupId',group_id)])
            response = self.post('/meetings/', data)

    def test_create_attendance(self):
        
        user_id = User.objects.all()
        meeting_id = User.objects.all()

        for user in user_id:
            for meeting in meeting_id:
                data = dict([('userId',user.id)]+[('meetingId',meeting.id)])
                response = self.post('/attendances/', data)
                self.assertEqual(response.status_code, 201)
   