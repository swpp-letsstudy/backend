import subprocess
import sys
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from study.models import StudyGroup


class Command(BaseCommand):
    help = 'Seeding database'

    def __init__(self):
        super().__init__()
        self.users = []
        self.study_groups = []

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
            env=os.environ.copy())

    def create_users(self):
        print("Create users")
        User.objects.create_superuser(
            username='superuser',
            email='superuser@superuser.com',
            password='1234')
        for i in range(3):
            User.objects.create_user(
                username='user{}'.format(i),
                email='a{}@a.com'.format(i),
                password='1234')
        self.users = User.objects.all()

    def create_groups(self):
        print("Create study groups")
        for user in self.users[1:]:
            for i in range(3):
                study_group = StudyGroup.objects.create(
                    name='group{}'.format(i),
                    info='group{} information'.format(i),
                    owner=user)
                study_group.members.set([user])
        self.study_groups = StudyGroup.objects.all()

    def handle(self, *args, **options):
        self.delete_database()
        self.migrate_database()
        self.create_users()
        self.create_groups()