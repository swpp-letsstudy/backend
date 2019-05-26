from rest_framework import serializers

from .models import StudyGroupNotice
from study.study_users.serializers import StudyUserSerializer


class StudyGroupNoticeSerializer(serializers.ModelSerializer):
    writer = StudyUserSerializer(read_only=True)

    class Meta:
        model = StudyGroupNotice
        fields = ('id', 'title', 'contents', 'writer')
