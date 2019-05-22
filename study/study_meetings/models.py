from django.db import models
from django.contrib.auth.models import User

from study.study_groups.models import StudyGroup


class StudyMeeting(models.Model):

    class Meta:
        ordering = ('time',)

    def __str__(self):
        return self.info

    created = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField()
    info = models.CharField(default='', max_length=100)
    group = models.ForeignKey(StudyGroup, related_name='meetings', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='study_meetings')
    # notices       StudyMeetingNotice  1:N
    # attendances   Attendance          1:N
    # files         StudyFile           1:N
    # tests         StudyTest           1:N
