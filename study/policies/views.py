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
        fines = Fine.objects.filter(meeting__group=studygroup, user=studyuser)
        for fine in fines:
            fine_sum += fine.policy.amount
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
        return Fine.objects.filter(policy__group=studygroup, user=studyuser)


class MyMeetingFineList(generics.ListAPIView):
    serializer_class = FineSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        meetingId = self.request.query_params.get('meetingId', None)
        if not StudyMeeting.objects.filter(pk=meetingId).exists():
            raise Http404
        studymeeting = StudyMeeting.objects.get(pk=meetingId)
        studyuser = StudyUser.objects.get(user=self.request.user)
        return Fine.objects.filter(meeting=studymeeting, user=studyuser)


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

