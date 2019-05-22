from rest_framework import serializers

from study.study_groups.models import StudyGroup


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
