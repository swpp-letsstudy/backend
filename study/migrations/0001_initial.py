# Generated by Django 2.2 on 2019-06-18 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=20)),
                ('info', models.CharField(default='', max_length=100)),
                ('is_open', models.BooleanField(default=False)),
                ('attendance_amount', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='StudyMeeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('time', models.DateTimeField()),
                ('info', models.CharField(default='', max_length=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_meetings', to='study.StudyGroup')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='StudyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default='', max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudyMeetingNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=20)),
                ('contents', models.CharField(max_length=200)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_meeting_notices', to='study.StudyMeeting')),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='study_meeting_notices', to='study.StudyUser')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='StudyGroupNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=20)),
                ('contents', models.CharField(max_length=200)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_group_notices', to='study.StudyGroup')),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='study_group_notices', to='study.StudyUser')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='studygroup',
            name='members',
            field=models.ManyToManyField(related_name='study_groups_join', to='study.StudyUser'),
        ),
        migrations.AddField(
            model_name='studygroup',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='study_groups_own', to='study.StudyUser'),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default='', max_length=20)),
                ('info', models.CharField(default='', max_length=100)),
                ('amount', models.IntegerField(default=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policies', to='study.StudyGroup')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fines', to='study.StudyMeeting')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fines', to='study.Policy')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fines', to='study.StudyUser')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='study.StudyMeeting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='study.StudyUser')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
