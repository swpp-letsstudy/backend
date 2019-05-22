from rest_framework import serializers

from study.study_groups.serializers import StudyGroupSerializer
from study.policies.models import Policy


class PolicySerializer(serializers.ModelSerializer):
    group = StudyGroupSerializer(read_only=True)
    fines = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Policy
        fields = ('id', 'name', 'group', 'fines')
