from django.http import Http404
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
        groupId = self.request.query_params.get('groupId', None)
        study_groups = StudyGroup.objects.filter(members__in=[user], id=groupId)
        return StudyMeeting.objects.filter(group__in=study_groups)

    def perform_create(self, serializer):
        user = self.request.user
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if user in group.members.all():
            serializer.save(group=group, members=[user])
        else:
            raise Http404


class StudyMeetingDetail(generics.RetrieveUpdateDestroyAPIView): # meetings/<int:pk>
    permission_classes = (IsAuthenticated, IsMeetingUser)
    queryset = StudyMeeting.objects.all()
    serializer_class = StudyMeetingSerializer
