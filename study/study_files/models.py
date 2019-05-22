from django.db import models
from django.contrib.auth.models import User

from study.study_groups.models import StudyGroup
from study.study_meetings.models import StudyMeeting


class StudyFile(models.Model):

    class Meta:
        ordering = ('created',)

    def __set__(self):
        return self.filepath

    created = models.DateTimeField(auto_now_add=True)

    filepath = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(StudyGroup, related_name='files', on_delete=models.CASCADE, null=True)
    meeting = models.ForeignKey(StudyMeeting, related_name='files', on_delete=models.CASCADE, null=True)
