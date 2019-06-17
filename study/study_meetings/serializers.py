from rest_framework import serializers

from .models import StudyMeeting
from study.study_users.serializers import StudyUserSerializer
from study.study_groups.models import StudyGroup
from study.study_groups.serializers import StudyGroupSerializer
from study.attendances.serializers import AttendanceSerializer

class StudyGroupMembersSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    members = StudyUserSerializer(many=True, read_only=True)

    class Meta:
        model = StudyGroup
        fields = ('id', 'owner', 'members')


class StudyMeetingSerializer(serializers.ModelSerializer):
    group = StudyGroupMembersSerializer(read_only=True)
    attendances = serializers.SlugRelatedField(many=True, read_only=True, slug_field='user_id')

    class Meta:
        model = StudyMeeting
        fields = ('id', 'time', 'info', 'group', 'attendances')
