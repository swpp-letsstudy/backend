from rest_framework import generics
from django.contrib.auth.models import User

from study.study_users.models import StudyUser
from study.study_meetings.models import StudyMeeting
from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceView(generics.CreateAPIView): # attendances/
    serializer_class = AttendanceSerializer
    '''
    { userId, meetingId } => toggle attendance 
    Toggle attendance with userId and meetingId.
    If an attendance instance exists, delete it.
    otherwise, create an new attendance instance.
    '''
    def perform_create(self, serializer):
        user = User.objects.filter(id=self.request.data['userId'])[0]
        user = StudyUser.objects.filter(user=user)[0]
        meeting = StudyMeeting.objects.filter(id=self.request.data['meetingId'])[0]
        attendances = Attendance.objects.filter(user=user, meeting=meeting)
        if attendances:
            attendances.delete()
        else:
            serializer.save(meeting=meeting, user=user)
