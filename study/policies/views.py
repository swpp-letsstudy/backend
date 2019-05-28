from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from study.study_users.models import StudyUser
from study.study_groups.models import StudyGroup
from study.study_meetings.models import StudyMeeting
from .models import Policy, MeetingFine, Fine
from .serializers import PolicySerializer, MeetingFineSerializer


class PolicyList(generics.ListCreateAPIView): # policies/?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s Policies
    # POST 
    serializer_class = PolicySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = StudyUser.objects.get(user=self.request.user)
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if not user in group.members.all():
            raise Http404
        return Policy.objects.filter(group=group)

    def perform_create(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if not user in group.members.all():
            raise Http404
        serializer.save(group=group)


class PolicyDetail(generics.RetrieveUpdateDestroyAPIView): # policies/<int:pk>/?groupId=<groupId>
    # GET get PolicySerializer(Policy(pk=pk)).data
    # PUT update Policy(pk=pk) with request.data
    # DELETE if user is member of group of policy, delete
    serializer_class = PolicySerializer
    permission_classes = (IsAuthenticated,)

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
        meeting = StudyMeeting.objects.get(id=meetingId)
        if not user in meeting.group.members.all():
            raise Http404
        return MeetingFine.objects.filter(meeting=meeting)

    def perform_create(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        meetingId = self.request.query_params.get('meetingId', None)
        meeting = StudyMeeting.objects.get(id=meetingId)
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

