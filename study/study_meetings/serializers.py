from rest_framework import serializers

from .models import StudyMeeting
from study.study_groups.serializers import StudyGroupSerializer
from study.users.serializers import StudyUserSimpleSerializer


class StudyMeetingSerializer(serializers.ModelSerializer):
    group = StudyGroupSerializer(read_only=True)
    members = StudyUserSimpleSerializer(many=True, read_only=True)
    notices = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    attendances = serializers.SlugRelatedField(many=True, read_only=True, slug_field='user_id')
    files = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tests = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudyMeeting
        fields = ('id', 'time', 'info', 'group', 'members', 'notices', 'attendances', 'files', 'tests')
