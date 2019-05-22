from rest_framework import serializers

from .models import StudyFile
from study.study_groups.serializers import StudyGroupSerializer

class StudyFileSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    group = StudyGroupSerializer(read_only=True)

    class Meta:
        model = StudyFile
        fields = ('id', 'filepath', 'owner', 'group')
