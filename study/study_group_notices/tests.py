from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from study.study_groups.models import StudyGroup
from study.study_group_notices.models import StudyGroupNotice

USERS_INFO = [{
    'username': 'user%d' % i,
    'password': '1234'
} for i in range(3)]


GROUPS_INFO = [{
    'name': 'group%d' % i,
    'info': 'info',
} for i in range(3)]

NOTICES_INFO = [{
    'title': 'title%d' % i,
    'contents': 'contents',
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

    def put(self, path, data):
        return self.client.put(path, data, **self.header())

    def create_group(self):
        for GROUP_INFO in GROUPS_INFO:
            self.post('/groups/', GROUP_INFO)

    def test_create_group_notice(self):
        self.login(USERS_INFO[0])

        self.create_group()

        group_id = StudyGroup.objects.all()[0].id 

        for NOTICE_INFO in NOTICES_INFO:
            data = dict(list(NOTICE_INFO.items()))
            response = self.post('/group_notices/?groupId=%d' % group_id, data)
            self.assertEqual(response.status_code, 201)

        response = self.get('/group_notices/?groupId=%d' % group_id)
        self.assertEqual(response.status_code, 200)

        notice_id = StudyGroupNotice.objects.all().filter(group_id = group_id)[0].id
        
        response = self.get('/group_notices/{}/?groupId={}'.format(notice_id, group_id))
        self.assertEqual(response.status_code, 200)

        data = {
            'title': 'titleupdate',
            'contents': 'contentsupdate',
        }
        response = self.put('/group_notices/{}/?groupId={}'.format(notice_id, group_id), data)
        self.assertEqual(response.status_code, 200)