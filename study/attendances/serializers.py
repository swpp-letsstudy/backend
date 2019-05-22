from rest_framework import serializers

from .models import Attendance
from study.study_meetings.serializers import StudyMeetingSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    meeting = StudyMeetingSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ('id', 'user', 'meeting')
