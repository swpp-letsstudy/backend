from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from study.study_users.models import StudyUser
from study.study_groups.models import StudyGroup
from study.study_meetings.models import StudyMeeting
from study.attendances.models import Attendance
from .models import *
from .serializers import *

class GetFineSum(APIView):
    # GET
    def get(self, request, format=None):
        groupId = self.request.query_params.get('groupId', None)
        if not StudyGroup.objects.filter(pk=groupId).exists():
            raise Http404
        studygroup = StudyGroup.objects.get(pk=groupId)
        studyuser = StudyUser.objects.get(user=self.request.user)
        meeting_fines = MeetingFine.objects.filter(policy__group=studygroup)
        fine_sum = 0
        for meeting_fine in meeting_fines:
            if Fine.objects.filter(meeting_fine=meeting_fine, user=studyuser).exists():
                fine_sum += meeting_fine.policy.amount
        attendance_amount = studygroup.attendance_amount
        for meeting in studygroup.study_meetings.all():
            if not Attendance.objects.filter(meeting=meeting, user=studyuser).exists():
                fine_sum += attendance_amount
        return Response(data=fine_sum, status=200)


class MyGroupFineList(generics.ListAPIView):
    serializer_class = FineSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        groupId = self.request.query_params.get('groupId', None)
        if not StudyGroup.objects.filter(pk=groupId).exists():
            raise Http404
        studygroup = StudyGroup.objects.get(pk=groupId)
        studyuser = StudyUser.objects.get(user=self.request.user)
        return Fine.objects.filter(meeting_fine__policy__group=studygroup, user=studyuser)


class MyMeetingFineList(generics.ListAPIView):
    serializer_class = FineSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        meetingId = self.request.query_params.get('meetingId', None)
        if not StudyMeeting.objects.filter(pk=meetingId).exists():
            raise Http404
        studymeeting = StudyMeeting.objects.get(pk=meetingId)
        meeting_fine = MeetingFine.objects.get(meeting=studymeeting)
        studyuser = StudyUser.objects.get(user=self.request.user)
        return Fine.objects.filter(meeting_fine=meeting_fine, user=studyuser)


class PolicyList(generics.ListCreateAPIView): # policies/?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s Policies
    # POST 
    serializer_class = PolicySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = StudyUser.objects.get(user=self.request.user)
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(pk=groupId)
        if not user in group.members.all():
            raise Http404
        return Policy.objects.filter(group=group)

    def perform_create(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(pk=groupId)
        if not user in group.members.all():
            raise Http404
        serializer.save(group=group)


class PolicyDetail(generics.RetrieveUpdateDestroyAPIView): # policies/<int:pk>/?groupId=<groupId>
    # GET get PolicySerializer(Policy(pk=pk)).data
    # PUT update Policy(pk=pk) with request.data
    # DELETE if user is member of group of policy, delete
    serializer_class = PolicySerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        groupId = self.request.query_params.get('groupId', None)
        if not StudyGroup.objects.filter(pk=groupId).exists():
            raise Http404
        studygroup = StudyGroup.objects.get(pk=groupId)
        return Policy.objects.filter(group=studygroup)

    def perform_update(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        policy = Policy.objects.get(pk=self.kwargs['pk'])
        if not user in policy.group.members.all():
            raise Http404
        serializer = PolicySerializer(policy, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise Http404

    def perform_destroy(self, request, *argc, **kwargs):
        user = StudyUser.objects.get(user=self.request.user)
        policy = Policy.objects.get(pk=self.kwargs['pk'])
        if not user in policy.group.members.all():
            raise Http404
        policy.delete()


class MeetingFineList(generics.ListCreateAPIView): # meeting_fines/?meetingId=<meetingId>
    # GET get StudyMeeting(id=meetingId)'s MeetingFines
    # POST 
    serializer_class = MeetingFineSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = StudyUser.objects.get(user=self.request.user)
        meetingId = self.request.query_params.get('meetingId', None)
        meeting = StudyMeeting.objects.get(pk=meetingId)
        if not user in meeting.group.members.all():
            raise Http404
        return MeetingFine.objects.filter(meeting=meeting)

    def perform_create(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        meetingId = self.request.query_params.get('meetingId', None)
        meeting = StudyMeeting.objects.get(pk=meetingId)
        if not user in meeting.group.members.all():
            raise Http404
        serializer.save(meeting=meeting)
    

class MeetingFineDetail(generics.RetrieveUpdateDestroyAPIView): # meeting_fines/<int:pk>/?meetingId=<meetingId>
    # GET get MeetingFineSerializer(MeetingFine(pk=pk)).data
    # PUT update MeetingFine(pk=pk) with request.data
    # DELETE if user is owner of group of MeetingFine, delete
    serializer_class = MeetingFineSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        meeting_fine = MeetingFine.objects.get(pk=self.kwargs['pk'])
        if not user in meeting_fine.meeting.group.members.all():
            raise Http404
        serializer = MeetingFineSerializer(meeting_fine, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise Http404

    def perform_destroy(self, request, *argc, **kwargs):
        user = StudyUser.objects.get(user=self.request.user)
        meeting_fine = MeetingFine.objects.get(pk=self.kwargs['pk'])
        if not user in meeting_fine.group.members.all():
            raise Http404
        meeting_fine.delete()

