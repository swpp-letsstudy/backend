from rest_framework import serializers

from .models import StudyMeeting
from study.study_users.serializers import StudyUserSerializer
from study.study_groups.serializers import StudyGroupSerializer

class StudyMeetingSerializer(serializers.ModelSerializer):
    group = StudyGroupSerializer(read_only=True)
    members = StudyUserSerializer(many=True, read_only=True)
    attendances = serializers.SlugRelatedField(many=True, read_only=True, slug_field='user__id')

    class Meta:
        model = StudyMeeting
        fields = ('id', 'time', 'info', 'group', 'members', 'attendances')
