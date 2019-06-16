from django.db import models

from study.study_users.models import StudyUser


class StudyGroup(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.name
    created = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(StudyUser, related_name='study_groups_own', on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(StudyUser, related_name='study_groups_join')
    name = models.CharField(max_length=20)
    info = models.CharField(default='', max_length=100)
    is_open = models.BooleanField(default=False)
