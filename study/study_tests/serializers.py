from rest_framework import serializers

from .models import StudyTest
from study.study_groups.serializers import StudyGroupSerializer
from study.study_meetings.serializers import StudyMeetingSerializer

class StudyTestSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    group = StudyGroupSerializer(read_only=True)
    meeting = StudyMeetingSerializer(read_only=True)

    class Meta:
        model = StudyTest
        fields = ('id', 'title', 'owner', 'group', 'meeting')
