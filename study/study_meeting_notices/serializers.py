from rest_framework import serializers

from .models import StudyMeetingNotice
from study.study_users.serializers import StudyUserSerializer


class StudyMeetingNoticeSerializer(serializers.ModelSerializer):
    writer = StudyUserSerializer(read_only=True)

    class Meta:
        model = StudyMeetingNotice
        fields = ('id', 'title', 'contents', 'writer')
