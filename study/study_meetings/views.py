from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from study.study_users.models import StudyUser
from study.study_groups.models import StudyGroup
from .models import StudyMeeting
from .serializers import StudyMeetingSerializer
from study.permissions import IsMeetingMember


class StudyMeetingList(generics.ListCreateAPIView): # meetings/?groupId=<groupId>
    # GET get StudyMeeting
    # POST { time, info }
    serializer_class = StudyMeetingSerializer

    def get_queryset(self):
        user = StudyUser.objects.get(user=self.request.user)
        groupId = self.request.query_params.get('groupId', None)
        study_groups = StudyGroup.objects.filter(members__in=[user], id=groupId)
        return StudyMeeting.objects.filter(group__in=study_groups)

    def perform_create(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if not user in group.members.all():
            raise Http404
        serializer.save(group=group, members=[user])


class StudyMeetingDetail(generics.RetrieveUpdateDestroyAPIView): # meetings/<int:pk>/?groupId=<groupId>
    permission_classes = (IsAuthenticated, IsMeetingMember)
    queryset = StudyMeeting.objects.all()
    serializer_class = StudyMeetingSerializer

class JoinExitMeeting(APIView):
    def get(self, request, format=None):
        meetingId = self.request.query_params.get('meetingId', None)
        if not StudyMeeting.objects.filter(pk=meetingId).exists():
            raise Http404
        studymeeting = StudyMeeting.objects.get(pk=meetingId)
        studyuser = StudyUser.objects.get(user=request.user)
        if not studyuser in studymeeting.group.members.all():
            raise Http404
        if studyuser in studymeeting.members.all():
            studymeeting.members.remove(studyuser)
            return Response('exited', status=200)
        else:
            studymeeting.members.add(studyuser)
            return Response('added', status=200)
