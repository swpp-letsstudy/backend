from django.db import models

from study.study_users.models import StudyUser
from study.study_groups.models import StudyGroup


class StudyMeeting(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.info
    created = models.DateTimeField(auto_now_add=True)

    group = models.ForeignKey(StudyGroup, related_name='study_meetings', on_delete=models.CASCADE)
    time = models.DateTimeField()
    info = models.CharField(default='', max_length=100)

