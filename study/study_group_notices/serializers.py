from rest_framework import serializers

from .models import StudyGroupNotice
from study.users.serializers import StudyUserSimpleSerializer


class StudyGroupNoticeSerializer(serializers.ModelSerializer):
    writer = StudyUserSimpleSerializer(read_only=True)
    group = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StudyGroupNotice
        fields = ('id', 'title', 'contents', 'writer', 'group')
