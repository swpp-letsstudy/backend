from rest_framework import serializers
from django.contrib.auth.models import User

from study.models import *

class StudyUserSerializer(serializers.ModelSerializer):
    studyGroups = serializers.PrimaryKeyRelatedField(many=True, queryset=StudyGroup.objects.all())

    class Meta:
        model = StudyUser
        fields = ('id', 'username', 'studyGroups')

class StudyGroupSerializer(serializers.ModelSerializer):
    meetings = serializers.PrimaryKeyRelatedField(many=True, queryset=StudyMeeting.objects.all())

    class Meta:
        model = StudyGroup
        fields = ('id', 'groupName', 'groupInfo', 'users', 'meetings')

class StudyMeetingSerializer(serializers.ModelSerializer):
    group = StudyGroupSerializer(read_only=True)
    
    class Meta:
        model = StudyMeeting
        fields = ('id', 'group', 'meetingTime', 'meetingName', 'meetingInfo')
