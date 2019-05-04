import subprocess
import sys
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seeding database'

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

    def handle(self, *args, **options):
        self.delete_database()
        self.migrate_database()
        self.create_users()