from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from study.study_users.models import StudyUser
from study.study_groups.models import StudyGroup
import datetime

class StudyMeeting(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.info
    created = models.DateTimeField(auto_now_add=True)

    group = models.ForeignKey(StudyGroup, related_name='study_meetings', on_delete=models.CASCADE)
    time = models.DateTimeField()
    info = models.CharField(default='', max_length=20)


@receiver(post_save, sender=StudyGroup)
def create_meeting(sender, instance, created, **kwargs):
    if created:
        day = instance.startday
        while day <= instance.endday:
            flag = False
            if day.weekday() is 0:
                if instance.monday is True:
                    flag = True
            if day.weekday() is 1:
                if instance.tuesday is True:
                    flag = True
            if day.weekday() is 2:
                if instance.wednesday is True:
                    flag = True
            if day.weekday() is 3:
                if instance.thursday is True:
                    flag = True
            if day.weekday() is 4:
                if instance.friday is True:
                    flag = True
            if day.weekday() is 5:
                if instance.saturday is True:
                    flag = True
            if day.weekday() is 6:
                if instance.sunday is True:
                    flag = True
                    
            if flag:
                StudyMeeting.objects.create(group=instance, time=datetime.datetime(day.year, day.month, day.day, instance.time.hour, instance.time.minute), info='Regular Meeting')
            day = day + datetime.timedelta(days=1)
