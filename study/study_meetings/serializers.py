from rest_framework import serializers

from .models import StudyMeeting


class StudyMeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyMeeting
        fields = ('id', 'time', 'info')
