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
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(StudyUser, related_name='study_groups')
