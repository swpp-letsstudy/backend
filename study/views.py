from rest_framework import generics
from study.serializers import *
from study.permissions import *

class StudyGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUser)
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer


class StudyGroupList(generics.ListCreateAPIView):
    serializer_class = StudyGroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUser)

    def get_queryset(self):
        user = self.request.user
        return StudyGroup.objects.filter(users__in=[user])

    def perform_create(self, serializer):
        serializer.save(users=[self.request.user])


class StudyMeetingList(generics.ListAPIView):
    queryset = StudyMeeting.objects.all()
    serializer_class = StudyMeetingSerializer
