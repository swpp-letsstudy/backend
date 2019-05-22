from django.db import models
from django.contrib.auth.models import User

from study.study_groups.models import StudyGroup
from study.study_meetings.models import StudyMeeting


class StudyTest(models.Model):

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=20)
    owner = models.ForeignKey(User, related_name='tests', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(StudyGroup, related_name='tests', on_delete=models.CASCADE, null=True)
    meeting = models.ForeignKey(StudyMeeting, related_name='tests', on_delete=models.CASCADE, null=True)
