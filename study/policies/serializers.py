from rest_framework import serializers

from study.study_users.serializers import StudyUserSerializer
from study.study_groups.serializers import StudyGroupSerializer
from study.policies.models import *


class PolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = Policy
        fields = ('id', 'name', 'amount')


class FineSerializer(serializers.ModelSerializer):
    user = StudyUserSerializer(read_only=True)
    
    class Meta:
        model = Fine
        fields = ('id', 'user', 'count')


class MeetingFineSerializer(serializers.ModelSerializer):
    policy = PolicySerializer(read_only=True)
    fines = FineSerializer(many=True, read_only=True)

    class Meta:
        model = MeetingFine
        fields = ('id', 'name', 'policy', 'fines')



