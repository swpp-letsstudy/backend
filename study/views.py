from rest_framework import generics, permissions
from django.contrib.auth.models import User

from study.models import *
from study.serializers import *
from study.permissions import *

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class StudyGroupList(generics.ListCreateAPIView):
    serializer_class = StudyGroupSerializer

    def get_queryset(self):
        user = self.request.user
        return StudyGroup.objects.filter(users__in=[user])

    def perform_create(self, serializer):
        serializer.save(users=[self.request.user])


class StudyMeetingList(generics.ListAPIView):
    queryset = StudyMeeting.objects.all()
    serializer_class = StudyMeetingSerializer
