from rest_framework import serializers

from .models import StudyUser
from study.users.serializers import UserSerializer


class StudyUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudyUser
        fields = ('id', 'user', 'nickname')
