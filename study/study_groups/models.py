from django.db import models
from django.contrib.auth.models import User


class StudyGroup(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.name
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=20)
    info = models.CharField(default='', max_length=100)
    owner = models.ForeignKey(User, related_name='study_groups_own', on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(User, related_name='study_groups_join')
    # notices           StudyGroupNotice    1:N
    # policies          Policy              1:N
    # meetings          StudyMeeting        1:N
    # files             StudyFeil           1:N
    # tests             StudyTest           1:N
