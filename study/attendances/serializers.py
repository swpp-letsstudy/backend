from rest_framework import serializers

from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    meeting = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Attendance
        fields = ('id', 'user', 'meeting')
