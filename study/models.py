from django.db import models
from django.contrib.auth.models import User

class StudyGroup(models.Model):
    class Meta:
        ordering = ('created',)

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20)
    info = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='study_groups')

class StudyMeeting(models.Model):
    class Meta:
        ordering = ('time',)

    created = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField()
    name = models.CharField(max_length=20)
    info = models.CharField(max_length=100)
    group = models.ForeignKey(StudyGroup, related_name='meetings', on_delete=models.CASCADE)
