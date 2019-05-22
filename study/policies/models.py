from django.db import models

from study.study_groups.models import StudyGroup


class Policy(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.name
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=20)
    group = models.ForeignKey(StudyGroup, related_name='policies', on_delete=models.CASCADE)
    # fines     Fine    1:N
