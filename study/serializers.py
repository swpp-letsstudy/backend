from rest_framework import serializers
from django.contrib.auth.models import User

from study.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'study_groups_own', 'study_groups_join')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        

class StudyGroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    meetings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudyGroup
        fields = ('id', 'name', 'info', 'owner', 'members', 'meetings')


class StudyMeetingSerializer(serializers.ModelSerializer):
    group = StudyGroupSerializer(read_only=True)
    attendances = serializers.SlugRelatedField(many=True, read_only=True, slug_field='user_id')

    class Meta:
        model = StudyMeeting
        fields = ('id', 'group', 'time', 'info', 'attendances')


class AttendanceSerializer(serializers.ModelSerializer):
    meeting = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Attendance
        fields = ('id', 'meeting', 'user')