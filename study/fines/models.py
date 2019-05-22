from django.db import models
from django.contrib.auth.models import User

from study.policies.models import Policy

class Fine(models.Model):
    class Meta:
        ordering = ('created',)
    def __str_(self):
        return self.user.username
    created = models.DateTimeField(auto_now_add=True)

    amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, related_name='fines', on_delete=models.CASCADE, null=True)
    policy = models.ForeignKey(Policy, related_name='fines', on_delete=models.CASCADE)
