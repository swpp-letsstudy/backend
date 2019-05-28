from django.db import models

from study.study_users.models import StudyUser
from study.study_meetings.models import StudyMeeting


class StudyMeetingNotice(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.title
    created = models.DateTimeField(auto_now_add=True)

    writer = models.ForeignKey(StudyUser, related_name='study_meeting_notices', on_delete=models.CASCADE, null=True)
    meeting = models.ForeignKey(StudyMeeting, related_name='study_meeting_notices', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    contents = models.CharField(max_length=200)
