from django.db import models

from study.study_users.models import StudyUser
import datetime

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
    attendance_amount = models.IntegerField(default=0)

    startday = models.DateField(default=datetime.date(2000,1,1))
    endday = models.DateField(default=datetime.date(2000,12,31))

    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    time =  models.TimeField(default = datetime.time(00,00,00))
