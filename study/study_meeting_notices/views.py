from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from study.study_users.models import StudyUser
from study.study_meetings.models import StudyMeeting
from .models import StudyMeetingNotice
from .serializers import StudyMeetingNoticeSerializer


class StudyMeetingNoticeList(generics.ListCreateAPIView): # meeting_notices/?meetingId=<meetingId>
    # GET get StudyMeeting(id=meetingId)'s StudyMeetingNotices
    # POST { title, contents } create request.user's StudyMeetingNotice
    serializer_class = StudyMeetingNoticeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = StudyUser.objects.get(user=self.request.user)
        meetingId = self.request.query_params.get('meetingId', None)
        meeting = StudyMeeting.objects.get(id=meetingId)
        if not user in meeting.group.members.all():
            raise Http404
        return StudyMeetingNotice.objects.filter(meeting=meeting)

    def perform_create(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        meetingId = self.request.query_params.get('meetingId', None)
        meeting = StudyMeeting.objects.get(id=meetingId)
        if not user in meeting.group.members.all():
            raise Http404
        serializer.save(writer=user, meeting=meeting)


class StudyMeetingNoticeDetail(generics.RetrieveUpdateDestroyAPIView): # meeting_notices/<int:pk>/?meetingId=<meetingId>
    # GET
    # PUT
    # DELETE
    serializer_class = StudyMeetingNoticeSerializer
    queryset = StudyMeetingNotice.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        meeting_notice = StudyMeetingNotice.objects.get(pk=self.kwargs['pk'])
        if meeting_notice.writer != user:
            raise Http404
        serializer = StudyMeetingSerializer(meeting_notice, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise Http404

    def perform_destroy(self, request, *argc, **kwargs):
        user = StudyUser.objects.get(user=self.request.user)
        meeting_notice = StudyMeetingNotice.objects.get(pk=self.kwargs['pk'])
        if not meeting_notice.writer == user:
            raise Http404
        meeting_notice.delete()
