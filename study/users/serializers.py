from django.contrib.auth.models import User
from rest_framework import serializers


class StudyUserSerializer(serializers.ModelSerializer):
    study_groups_own = serializers.StringRelatedField(many=True, read_only=True)
    study_groups_join = serializers.StringRelatedField(many=True, read_only=True)
    group_notices = serializers.StringRelatedField(many=True, read_only=True)
    fines = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    study_meetings = serializers.StringRelatedField(many=True, read_only=True)
    meeting_notices = serializers.StringRelatedField(many=True, read_only=True)
    attendances = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    files = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tests = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'study_groups_own', 'study_groups_join', 'group_notices', 'fines', 'study_meetings', 'meeting_notices', 'attendances', 'files', 'tests')


class StudyUserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
