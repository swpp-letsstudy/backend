import datetime, pytz, subprocess, sys, os, random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from study.study_user_settings.models import StudyUserSetting
from study.study_groups.models import StudyGroup
from study.study_group_notices.models import StudyGroupNotice
from study.policies.models import Policy
from study.fines.models import Fine
from study.study_meetings.models import StudyMeeting
from study.attendances.models import Attendance
from study.study_meeting_notices.models import StudyMeetingNotice
from study.study_files.models import StudyFile
from study.study_tests.models import StudyTest


class Command(BaseCommand):
    help = 'Seeding database'

    def __init__(self):
        super().__init__()

    def delete_database(self):
        print('Delete database')
        subprocess.check_call(['rm', '-rf', 'db.sqlite3'])

    def migrate_database(self):
        print('Migrate database')
        python_executable = sys.executable
        project_path = os.getcwd()
        manage_py_path = '{}/manage.py'.format(project_path)
        subprocess.check_call(
            [python_executable, manage_py_path, 'migrate'],
            env=os.environ.copy()
        )

    def create_superuser(self):
        print("Create Superuser")
        User.objects.create_superuser(
            username='superuser',
            email='superuser@superuser.com',
            password='1234'
        )
        self.superuser = User.objects.all()[0]

    def create_users(self):
        print("Create Users")
        for i in range(1, 6):
            User.objects.create_user(
                username='user%d' % i,
                email='a%d@a.com' % i,
                password='1234'
            )
        self.users = User.objects.all()[1:]

    def create_user_settings(self):
        print("Modify StudyUserSettings")
        for user in User.objects.all():
            study_user_setting = StudyUserSetting.objects.get(user=user)
            study_user_setting.info = 'info %s' % user.username
            study_user_setting.save()
        self.study_user_settings = StudyUserSetting.objects.all()

    def create_groups(self):
        print("Create StudyGroups")
        for i in range(1, 6):
            user = User.objects.get(id=i+1)
            study_group = StudyGroup.objects.create(
                name='group%d' % i,
                info='info group%d' % i,
                owner=user,
            ).members.set([user])
        for i in range(1, 6):
            user = User.objects.get(id=i%5+2)
            study_group = StudyGroup.objects.get(id=i)
            study_group.members.add(user)
        self.study_groups = StudyGroup.objects.all()

    def create_group_notices(self):
        print("Create StudyGroupNotices")
        for study_group in self.study_groups:
            for user in study_group.members.all():
                StudyGroupNotice.objects.create(
                    title='title %s %s' % (study_group.name, user.username),
                    contents='contents %s %s' % (study_group.name, user.username),
                    writer=user,
                    group=study_group
                )

    def create_policies(self):
        print("Create Policies")
        for study_group in self.study_groups:
            for i in range(1, 3):
                Policy.objects.create(
                    name='name %s-%d' % (study_group.name, i),
                    group=study_group
                )
        self.policies = Policy.objects.all()

    def create_fines(self):
        print("Create Fines")
        for policy in self.policies:
            for user in policy.group.members.all():
                Fine.objects.create(
                    amount=random.randrange(1, 10),
                    user=user,
                    policy=policy
                )

    def create_meetings(self):
        print("Create StudyMeetings")
        for study_group in StudyGroup.objects.all():
            for user in study_group.members.all():
                StudyMeeting.objects.create(
                    time=datetime.datetime.now(pytz.utc),
                    info='info %s %s' % (study_group.name, user.username),
                    group=study_group
                ).members.set(study_group.members.all())
        self.study_meetings = StudyMeeting.objects.all()

    def create_meeting_notices(self):
        print("Create StudyMeetingNotices")
        for meeting in self.study_meetings:
            for user in meeting.members.all():
                StudyMeetingNotice.objects.create(
                    title='title %s %s' % (meeting.group.name, user.username),
                    contents='contents %s %s' % (meeting.group.name, user.username),
                    writer=user,
                    meeting=meeting
                )
    
    def create_attendances(self):
        print("Create Attendances")
        for meeting in self.study_meetings:
            for user in meeting.members.all():
                Attendance.objects.create(
                    user=user,
                    meeting=meeting
                )
    
    def create_files(self):
        print("Create StudyFiles")
        for group in self.study_groups:
            for user in group.members.all():
                StudyFile.objects.create(
                    filepath='/file/%s/%s/%d.txt' % (group.name, user.username, random.randrange(1, 10)),
                    owner=user,
                    group=group
                )

    def create_tests(self):
        print("Create StudyTests")
        for group in self.study_groups:
            for meeting in group.meetings.all():
                for user in meeting.members.all():
                    StudyTest.objects.create(
                        title='title %d %d %s' % (group.id, meeting.id, user.username),
                        owner=user,
                        group=group,
                        meeting=meeting
                    )

    def handle(self, *args, **options):
        self.delete_database()
        self.migrate_database()
        self.create_superuser()
        self.create_users()
        self.create_user_settings()
        self.create_groups()
        self.create_group_notices()
        self.create_policies()
        self.create_fines()
        self.create_meetings()
        self.create_meeting_notices()
        self.create_attendances()
        self.create_files()
        self.create_tests()
