from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class StudyUserSetting(models.Model):
    def __str__(self):
        return self.user.username
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.CharField(default='', max_length=50)


@receiver(post_save, sender=get_user_model())
def create_user_studyusersetting(sender, instance, created, **kwargs):
    if created:
        StudyUserSetting.objects.create(user=instance)
