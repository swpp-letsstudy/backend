from urllib.parse import parse_qs
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import StudyMeeting
from study.study_meetings.serializers import StudyMeetingSerializer
from study.study_groups.models import StudyGroup
from study.permissions import IsMeetingUser


class StudyMeetingList(generics.ListCreateAPIView): # meetings/
    # GET get StudyMeeting
    # POST { time, info }
    serializer_class = StudyMeetingSerializer
    def get_queryset(self):
        user = self.request.user
        groupId = parse_qs(self.request.GET.urlencode())['groupId'][0]
        study_groups = StudyGroup.objects.filter(members__in=[user], id=groupId)
        return StudyMeeting.objects.filter(group__in=study_groups)

    def perform_create(self, serializer):
        user = self.request.user
        group = StudyGroup.objects.filter(id=self.request.data['groupId'])[0]
        serializer.save(group=group, members=[user])


class StudyMeetingDetail(generics.RetrieveUpdateDestroyAPIView): # meetings/<int:pk>
    permission_classes = (IsAuthenticated, IsMeetingUser)
    queryset = StudyMeeting.objects.all()
    serializer_class = StudyMeetingSerializer
