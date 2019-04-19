from rest_framework import serializers
from django.contrib.auth.models import User

from study.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'study_groups')

class StudyGroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    meetings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudyGroup
        fields = ('id', 'name', 'info', 'users', 'meetings')

class StudyMeetingSerializer(serializers.ModelSerializer):
    group = StudyGroupSerializer(read_only=True)

    class Meta:
        model = StudyMeeting
        fields = ('id', 'group', 'time', 'name', 'info')
