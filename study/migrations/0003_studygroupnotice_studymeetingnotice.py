# Generated by Django 2.2 on 2019-05-11 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_auto_20190509_0708'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyMeetingNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=20)),
                ('contents', models.CharField(max_length=200)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notices', to='study.StudyMeeting')),
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
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notices', to='study.StudyGroup')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
