from django.db import models

from study.study_users.models import StudyUser
from study.study_groups.models import StudyGroup
from study.study_meetings.models import StudyMeeting


class Policy(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.name
    created = models.DateTimeField(auto_now_add=True)

    group = models.ForeignKey(StudyGroup, related_name='policies', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    amount = models.IntegerField(default=1)


class MeetingFine(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.name
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=20)
    policy = models.ForeignKey(Policy, related_name='meeting_fines', on_delete=models.CASCADE)
    meeting = models.ForeignKey(StudyMeeting, related_name='meeting_fines', on_delete=models.CASCADE)


class Fine(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.user
    created = models.DateTimeField(auto_now_add=True)

    meeting_fine = models.ForeignKey(MeetingFine, related_name='fines', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(StudyUser, related_name='fines', on_delete=models.CASCADE, null=True)
    count = models.IntegerField(default=0)
