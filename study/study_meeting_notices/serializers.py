from rest_framework import serializers

from .models import StudyMeetingNotice


class StudyMeetingNoticeSerializer(serializers.ModelSerializer):
    writer = serializers.PrimaryKeyRelatedField(read_only=True)
    meeting = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StudyMeetingNotice
        fiels = ('id', 'title', 'contents', 'writer', 'meeting')
