from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from datetime import datetime, timezone

from study.study_users.models import StudyUser
from study.study_meetings.models import StudyMeeting
from study.study_groups.models import StudyGroup


USERS_INFO = [{
    'username': 'user%d' % i,
    'password': '1234'
} for i in range(3)]


GROUPS_INFO = [{
    'name': 'group%d' % i,
    'info': 'info',
} for i in range(3)]


MEETINGS_INFO = [{
    'time': datetime.now(timezone.utc).replace(second=0, microsecond=0),
    'info': 'info%d' % i,
} for i in range(3)]


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
        return {'HTTP_AUTHORIZATION': 'Token %s' % self.token} if self.token else {}

    def get(self, path):
        return self.client.get(path, **self.header())

    def post(self, path, data):
        return self.client.post(path, data, **self.header())

    def create_group(self, group_info):
        self.post('/groups/', group_info)
        return self.get('/groups/')

    def create_meeting(self):
        self.login(USERS_INFO[0])
        for GROUP_INFO in GROUPS_INFO:
            self.create_group(GROUP_INFO)

        groupId = StudyGroup.objects.all()[0].id

        for MEETING_INFO in MEETINGS_INFO:
            self.post('/meetings/?groupId=%d' % groupId, MEETING_INFO)

    def test_create_attendance(self):
        meetings = StudyMeeting.objects.all()

        for meeting in meetings:
            for user in meeting.group.members.all():
                data = {
                    'userId': user.id,
                    'meetingId': meeting.id
                }
                response = self.post('/attendance/', data)
                self.assertEqual(response.status_code, 201)
