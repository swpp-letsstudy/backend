from django.db import models

from study.study_users.models import StudyUser
from study.study_groups.models import StudyGroup


class StudyGroupNotice(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.title
    created = models.DateTimeField(auto_now_add=True)

    writer = models.ForeignKey(StudyUser, related_name='study_group_notices', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(StudyGroup, related_name='study_group_notices', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    contents = models.CharField(max_length=200)
