from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from .serializers import StudyMeetingNoticeSerializer
from .models import StudyMeetingNotice
from study.study_meetings.models import StudyMeeting
from study.study_meetings.serializers import StudyMeetingSerializer


class StudyMeetingNoticeList(generics.ListCreateAPIView): # meeting_notices/?meetingId=<meetingId>
    # GET get StudyMeeting(id=meetingId)'s StudyMeetingNotices
    # POST { title, contents } create request.user's StudyMeetingNotice
    serializer_class = StudyMeetingNoticeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        meetingId = self.request.query_params.get('meetingId', None)
        meeting = StudyMeeting.objects.get(id=meetingId)
        if not self.request.user in meeting.members.all():
            raise Http404
        return StudyMeetingNotice.objects.filter(meeting=meeting)

    def perform_create(self, serializer):
        user = self.request.user
        meetingId = self.request.query_params.get('meetingId', None)
        meeting = StudyMeeting.objects.get(id=meetingId)
        if user in meeting.members.all():
            serializer.save(writer=user, meeting=meeting)
        else:
            raise Http404


class StudyMeetingNoticeDetail(generics.RetrieveDestroyAPIView): # meeting_notices/<int:pk>/?meetingId=<meetingId>
    # GET
    # PUT
    # DELETE
    serializer_class = StudyMeetingNoticeSerializer
    queryset = StudyMeetingNotice.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        user = self.request.user
        notice = StudyMeetingNotice.objects.get(pk=self.kwargs['pk'])
        if notice.writer != user:
            raise Http404
        serializer = StudyMeetingSerializer(notice, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise Http404

    def perform_destroy(self, request, *argc, **kwargs):
        user = self.request.user
        notice = StudyMeetingNotice.objects.get(pk=self.kwargs['pk'])
        if notice.writer == user:
            notice.delete()
        else:
            raise Http404
