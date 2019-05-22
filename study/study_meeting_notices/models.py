from django.db import models
from django.contrib.auth.models import User

from study.study_meetings.models import StudyMeeting


class StudyMeetingNotice(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.title
    created = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=20)
    contents = models.CharField(max_length=200)
    writer = models.ForeignKey(User, related_name='meeting_notices', on_delete=models.CASCADE, null=True)
    meeting = models.ForeignKey(StudyMeeting, related_name='notices', on_delete=models.CASCADE)
