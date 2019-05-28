from django.db import models

from study.study_users.models import StudyUser
from study.study_meetings.models import StudyMeeting


class Attendance(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.user.nickname
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(StudyUser, related_name='attendances', on_delete=models.CASCADE)
    meeting = models.ForeignKey(StudyMeeting, related_name='attendances', on_delete=models.CASCADE)
