from django.db import models
from django.contrib.auth.models import User

class StudyUser(User):
    class Meta:
        ordering = ('created',)

    created = models.DateTimeField(auto_now_add=True)

class StudyGroup(models.Model):
    class Meta:
        ordering = ('created',)

    created = models.DateTimeField(auto_now_add=True)
    groupname = models.CharField(max_length=100)
    users = models.ManyToManyField(StudyUser, related_name='studyGroups')

class StudyMeeting(models.Model):
    class Meta:
        ordering = ('meetingTime')

    created = models.DateTimeField(auto_now_add=True)
    meetingTime = models.DateTimeField()
    group = models.ForeignKey(StudyGroup, related_name='meetings', on_delete=models.CASCADE)
