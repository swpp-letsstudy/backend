from rest_framework import generics, permissions
from django.contrib.auth.models import User

from study.models import *
from study.serializers import *
from study.permissions import *

class StudyGroupUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUser)
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer

class StudyGroupCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUser)
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer

class StudyGroupList(generics.ListAPIView):
    serializer_class = StudyGroupSerializer
    def get_queryset(self):
        user = self.request.user
        return StudyGroup.objects.filter(users__in=[user])

class StudyMeetingList(generics.ListAPIView):
    queryset = StudyMeeting.objects.all()
    serializer_class = StudyMeetingSerializer
