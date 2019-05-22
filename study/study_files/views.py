from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import StudyFileSerializer
from study.study_groups.models import StudyGroup
from study.study_files.models import StudyFile
from study.study_meetings.models import StudyMeeting
from study.study_tests.serializers import StudyTestSerializer


class StudyGroupFileList(generics.ListCreateAPIView): # group_files?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s file list
    # POST { filepath }
    serializer_class = StudyFileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if user in group.members.all():
            return StudyFile.objects.filter(group=group)
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


class StudyMeetingFileList(generics.ListCreateAPIView): # meeting_files?meetingId=<meetingId>
    # GET get StudyMeeting(id=meetingId)'s file list
    serializer_class = StudyFileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        meetingId = self.request.query_params.get('meetingId', None)
        meeting = StudyMeeting.objects.get(id=meetingId)
        if user in meeting.members.all():
            return StudyFile.objects.filter(meeting=meeting)
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


class StudyFileDetail(generics.RetrieveUpdateDestroyAPIView): # files/<int:pk>/
    serializer_class = StudyTestSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, request, *argc, **kwargs):
        user = self.request.user
        studyfile = StudyFile.objects.get(pk=self.kwargs['pk'])
        if studyfile.owner == user:
            studyfile.delete()
        else:
            raise Http404
