from rest_framework import serializers

from .models import StudyUserSetting
from study.users.serializers import StudyUserSerializer


class StudyUserSettingSerializer(serializers.ModelSerializer):
    user = StudyUserSerializer(read_only=True)

    class Meta:
        model = StudyUserSetting
        fields = ('id', 'user', 'info')
