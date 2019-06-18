import datetime
from pytz import utc
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


class StudyMeetingListFew(generics.ListAPIView):
    serializer_class = StudyMeetingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = StudyUser.objects.get(user=self.request.user)
        groupId = self.request.query_params.get('groupId', None)
        num = self.request.query_params.get('num', None)
        try:
            num = int(num)
        except ValueError:
            raise Http404
        if not StudyGroup.objects.filter(members__in=[user], pk=groupId).exists():
            raise Http404
        studygroups = StudyGroup.objects.get(members__in=[user], pk=groupId)
        studymeetings = StudyMeeting.objects.filter(group=studygroups)
        now = datetime.datetime.now(utc) + datetime.timedelta(hours=9)
        few_studymeetings = []
        cnt = 0
        for studymeeting in studymeetings:
            if now < studymeeting.time:
                few_studymeetings.append(studymeeting)
                cnt += 1
                if cnt == num*3+3:
                    break
        return few_studymeetings


class StudyMeetingList(generics.ListCreateAPIView): # meetings/?groupId=<groupId>
    # GET get StudyMeeting
    # POST { time, info }
    serializer_class = StudyMeetingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = StudyUser.objects.get(user=self.request.user)
        groupId = self.request.query_params.get('groupId', None)
        study_groups = StudyGroup.objects.filter(members__in=[user], pk=groupId)
        return StudyMeeting.objects.filter(group__in=study_groups)

    def perform_create(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if not user in group.members.all():
            raise Http404
        serializer.save(group=group)


class StudyMeetingDetail(generics.RetrieveDestroyAPIView): # meetings/<int:pk>/?groupId=<groupId>
    permission_classes = (IsAuthenticated, IsMeetingMember)
    queryset = StudyMeeting.objects.all()
    serializer_class = StudyMeetingSerializer
    