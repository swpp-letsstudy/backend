from rest_framework import serializers
from study.models import *


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


class StudyUserSettingSerializer(serializers.ModelSerializer):
    user = StudyUserSerializer(read_only=True)

    class Meta:
        model = StudyUserSetting
        fields = ('id', 'user', 'info')


class StudyGroupSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    members = serializers.StringRelatedField(many=True, read_only=True)
    notices = serializers.StringRelatedField(many=True, read_only=True)
    # policies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # meetings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # files = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # tests = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudyGroup
        fields = ('id', 'name', 'info', 'owner', 'members', 'notices')
        # , 'policies', 'meetings', 'files', 'tests'


class StudyGroupNoticeSerializer(serializers.ModelSerializer):
    writer = serializers.PrimaryKeyRelatedField(read_only=True)
    group = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = StudyGroupNotice
        fields = ('id', 'title', 'contents', 'writer', 'group')


class PolicySerializer(serializers.ModelSerializer):
    group = StudyGroupSerializer(read_only=True)
    fines = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Policy
        fields = ('id', 'name', 'group', 'fines')


class FineSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    policy = PolicySerializer(read_only=True)

    class Meta:
        model = Fine
        fields = ('id', 'amount', 'user', 'policy')


class StudyMeetingSerializer(serializers.ModelSerializer):
    group = StudyGroupSerializer(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    notices = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    attendances = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tests = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudyMeeting
        fields = ('id', 'time', 'info', 'group', 'members', 'notices', 'attendances', 'tests')


class StudyMeetingNoticeSerializer(serializers.ModelSerializer):
    writer = serializers.PrimaryKeyRelatedField(read_only=True)
    meeting = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StudyMeetingNotice
        fiels = ('id', 'title', 'contents', 'writer', 'meeting')


class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    meeting = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Attendance
        fields = ('id', 'user', 'meeting')


class StudyFileSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    group = StudyGroupSerializer(read_only=True)

    class Meta:
        model = StudyFile
        fields = ('id', 'filepath', 'owner', 'group')


class StudyTestSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    group = StudyGroupSerializer(read_only=True)
    meeting = StudyMeetingSerializer(read_only=True)

    class Meta:
        model = StudyTest
        fields = ('id', 'title', 'owner', 'group', 'meeting')
