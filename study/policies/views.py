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
        fine_sum = 0
        for fine in fines:
            fine_sum += fine.policy.amount
        attendance_amount = studygroup.attendance_amount
        for meeting in studygroup.study_meetings.all():
            if not Attendance.objects.filter(meeting=meeting, user=studyuser).exists():
                fine_sum += attendance_amount
        return Response(data=fine_sum, status=200)


class MyGroupFineList(generics.ListAPIView):
    # GET
    def get(self, request, format=None):
        groupId = self.request.query_params.get('groupId', None)
        if not StudyGroup.objects.filter(pk=groupId).exists() or not StudyUser.objects.filter(user=request.user):
            raise Http404
        studygroup = StudyGroup.objects.get(pk=groupId)
        studyuser = StudyUser.objects.get(user=request.user)
        ret = {}
        for fine in Fine.objects.filter(policy__group=studygroup, user=studyuser):
            if not fine.meeting.info in ret:
                ret[fine.meeting.info] = []
            ret[fine.meeting.info].append({
                'id': fine.id,
                'policy': {
                    'id': fine.policy.id,
                    'name': fine.policy.name,
                    'amount': fine.policy.amount
                }
            })
        return Response(data=ret, status=200)


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


class ManageFine(APIView):
    # GET
    def get(self, request, format=None):
        userId = self.request.query_params.get('userId', None)
        meetingId = self.request.query_params.get('meetingId', None)
        policyId = self.request.query_params.get('policyId', None)
        if not StudyUser.objects.filter(pk=userId).exists() or not StudyMeeting.objects.filter(pk=meetingId).exists() or not Policy.objects.filter(pk=policyId).exists():
            raise Http404
        studyuser = StudyUser.objects.get(pk=userId)
        studymeeting = StudyMeeting.objects.get(pk=meetingId)
        policy = Policy.objects.get(pk=policyId)
        if not Fine.objects.filter(user=studyuser, meeting=studymeeting, policy=policy).exists():
            fine = Fine(user=studyuser, meeting=studymeeting, policy=policy)
            fine.save()
        else:
            Fine.objects.get(user=studyuser, meeting=studymeeting, policy=policy).delete()
        return Response(status=200)


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

