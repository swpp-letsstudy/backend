import datetime, pytz, subprocess, sys, os, random
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from study.study_users.models import StudyUser
from study.study_groups.models import StudyGroup
from study.study_group_notices.models import StudyGroupNotice
from study.study_meetings.models import StudyMeeting
from study.study_meeting_notices.models import StudyMeetingNotice
from study.attendances.models import Attendance
from study.policies.models import Policy, Fine


class Command(BaseCommand):
    help = 'Seeding database'

    def __init__(self):
        super().__init__()
        self.now = datetime.datetime.now(pytz.utc).replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(hours=9)

    def delete_database(self):
        print('Delete database')
        subprocess.check_call(['rm', '-rf', 'db.sqlite3'])

    def migrate_database(self):
        print('Migrate database')
        python_executable = sys.executable
        project_path = os.getcwd()
        manage_py_path = '%s/manage.py' % project_path
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
        self.superuser = User.objects.get(username='superuser')

    def create_users(self):
        print("Create Users")
        for i in range(1, 6):
            User.objects.create_user(
                username='user%d' % i,
                email='a%d@a.com' % i,
                password='1234'
            )
        self.users = User.objects.filter(username__startswith='user')

    def modify_studyusers(self):
        print("Modify StudyUsers")
        for user in self.users:
            i = user.username[-1]
            study_user = StudyUser.objects.get(user=user)
            study_user.nickname = 'nickname%c' % i
            study_user.save()
        self.study_users = StudyUser.objects.filter(user__in=self.users)

    def create_groups(self):
        print("Create StudyGroups")
        for user in self.study_users:
            i = user.nickname[-1]
            study_group = StudyGroup.objects.create(
                name='group%c' % i,
                info='group%c info' % i,
                owner=user,
                startday=self.now - relativedelta(months=1),
                endday=self.now + relativedelta(months=1),
                monday=True,
                time=datetime.time(random.randint(0, 23), 0, 0)
            ).members.set([user])
        for i in range(1, 6):
            study_group = StudyGroup.objects.get(name='group%d'%i)
            study_user = StudyUser.objects.get(nickname='nickname%d'%(i%5+1))
            study_group.members.add(study_user)
        self.study_groups = StudyGroup.objects.all()


    def handle(self, *args, **options):
        self.delete_database()
        self.migrate_database()
        self.create_superuser()
        self.create_users()
        self.modify_studyusers()
        self.create_groups()
