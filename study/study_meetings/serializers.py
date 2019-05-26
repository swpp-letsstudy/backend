from rest_framework import serializers

from .models import StudyMeeting
from study.study_users.serializers import StudyUserSerializer
from study.study_groups.serializers import StudyGroupSerializer
from study.attendances.serializers import AttendanceSerializer

class StudyMeetingSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(read_only=True, slug_field='id')
    members = StudyUserSerializer(many=True, read_only=True)
    attendances = serializers.SlugRelatedField(many=True, read_only=True, slug_field='user_id')

    class Meta:
        model = StudyMeeting
        fields = ('id', 'time', 'info', 'group', 'members', 'attendances')
