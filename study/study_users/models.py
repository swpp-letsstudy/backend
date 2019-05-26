from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class StudyUser(models.Model):
    def __str__(self):
        return self.nickname
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(default='', max_length=15)


@receiver(post_save, sender=get_user_model())
def create_user_studyuser(sender, instance, created, **kwargs):
    if created:
        StudyUser.objects.create(user=instance, nickname=instance.username)

