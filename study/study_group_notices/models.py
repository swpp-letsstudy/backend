from django.db import models
from django.contrib.auth.models import User

from study.study_groups.models import StudyGroup


class StudyGroupNotice(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.title
    created = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=20)
    contents = models.CharField(max_length=200)
    writer = models.ForeignKey(User, related_name='group_notices', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(StudyGroup, related_name='notices', on_delete=models.CASCADE)
