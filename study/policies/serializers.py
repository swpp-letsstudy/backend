from rest_framework import serializers

from study.study_users.serializers import StudyUserSerializer
from study.study_groups.serializers import StudyGroupSerializer
from study.study_meetings.serializers import StudyMeetingSerializer
from study.policies.models import *


class PolicySerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Policy
        fields = ('id', 'group', 'name', 'info', 'amount')


class FineSerializer(serializers.ModelSerializer):
    policy = PolicySerializer(read_only=True)
    meeting = StudyMeetingSerializer(read_only=True)
    user = StudyUserSerializer(read_only=True)
    
    class Meta:
        model = Fine
        fields = ('id', 'policy', 'meeting', 'user')

