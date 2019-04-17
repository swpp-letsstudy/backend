from rest_framework import serializers
from django.contrib.auth.models import User

from study.models import *

class StudyUserSerializer(serializers.ModelSerializer):
    studyGroups = serializers.PrimaryKeyRelatedField(many=True, queryset=StudyGroup.objects.all())

    class Meta:
        model = StudyGroup
        fields = ('id', 'username', 'studyGroups')

class StudyGroupSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=StudyUser.objects.all())
    meetings = serializers.PrimaryKeyRelatedField(many=True, queryset=StudyMeeting.objects.all())

    class Meta:
        model = StudyGroup
        fields = ('id', 'groupname', 'users', 'meetings')

class StudyMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMeeting
        fields = ('id',)

