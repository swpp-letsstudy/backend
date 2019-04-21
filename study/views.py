from rest_framework import generics
from study.serializers import *
from study.permissions import *
from urllib.parse import parse_qs

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


class StudyMeetingList(generics.ListCreateAPIView):
    serializer_class = StudyMeetingSerializer

    def get_queryset(self):
        user = self.request.user
        groupId = parse_qs(self.request.GET.urlencode())['groupId'][0]
        study_groups = StudyGroup.objects.filter(users__in=[user], id=groupId)
        return StudyMeeting.objects.filter(group__in=study_groups)

    def perform_create(self, serializer):
        group = StudyGroup.objects.filter(id=self.request.data['groupId'])[0]
        serializer.save(group=group)


class AttendanceCreate(generics.CreateAPIView):
    serializer_class = AttendanceSerializer

    def perform_create(self, serializer):
        user=User.objects.filter(id=self.request.data['userId'])[0]
        meeting = StudyMeeting.objects.filter(id=self.request.data['meetingId'])[0]
        serializer.save(meeting=meeting, user=user)