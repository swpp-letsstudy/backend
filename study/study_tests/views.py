from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import StudyTest
from .serializers import StudyTestSerializer
from study.study_groups.models import StudyGroup
from study.study_meetings.models import StudyMeeting


class StudyGroupTestList(generics.ListCreateAPIView): # group_tests?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s file list
    # POST { title }
    serializer_class = StudyTestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if user in group.members.all():
            return StudyTest.objects.filter(group=group)
        else:
            raise Http404

    def perform_create(self, serializer):
        user = self.request.user
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if user in group.members.all():
            serializer.save(owner=user, group=group)
        else:
            raise Http404


class StudyMeetingTestList(generics.ListCreateAPIView): # meeting_tests?meetingId=<meetingId>
    # GET get StudyMeeting(id=meetingId)'s file list
    serializer_class = StudyTestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        meetingId = self.request.query_params.get('meetingId', None)
        meeting = StudyMeeting.objects.get(id=meetingId)
        if user in meeting.members.all():
            return StudyTest.objects.filter(meeting=meeting)
        else:
            raise Http404

    def perform_create(self, serializer):
        user = self.request.user
        meetingId = self.request.query_params.get('meetingId', None)
        meeting = StudyMeeting.objects.get(id=meetingId)
        if user in meeting.members.all():
            serializer.save(owner=user, meeting=meeting)
        else:
            raise Http404


class StudyTestDetail(generics.RetrieveUpdateDestroyAPIView): # tests/<int:pk>/
    serializer_class = StudyTestSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, request, *argc, **kwargs):
        user = self.request.user
        studytest = StudyTest.objects.get(pk=self.kwargs['pk'])
        if studytest.owner == user:
            studytest.delete()
        else:
            raise Http404
