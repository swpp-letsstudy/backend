from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from study.study_users.models import StudyUser
from .models import StudyGroup
from .serializers import StudyGroupSerializer
from study.attendances.models import Attendance
from study.permissions import IsGroupMember

class SetAttendanceFine(APIView):
    # GET
    def get(self, request, format=None):
        groupId = self.request.query_params.get('groupId', None)
        try:
            amount = int(self.request.query_params.get('amount', None))
        except ValueError:
            raise Http404
        if amount < 0:
            raise Http404
        if not StudyGroup.objects.filter(pk=groupId).exists():
            raise Http404
        studygroup = StudyGroup.objects.get(pk=groupId)
        studygroup.attendance_amount = amount
        studygroup.save()
        return Response('successed', status=200)


class GetAttendanceFine(APIView):
    # GET
    def get(self, request, format=None):
        studyuser = StudyUser.objects.get(user=request.user)
        groupId = self.request.query_params.get('groupId', None)
        if not StudyGroup.objects.filter(pk=groupId).exists():
            raise Http404
        studygroup = StudyGroup.objects.get(pk=groupId)
        if not studyuser in studygroup.members.all():
            raise Http404
        return Response(data=studygroup.attendance_amount, status=200)


class StudyGroupList(generics.ListCreateAPIView): # groups/
    # GET get user's StudyGroups
    # POST { name, info }, create user's StudyGroup
    serializer_class = StudyGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = StudyUser.objects.get(user=self.request.user)
        return StudyGroup.objects.filter(members__in=[user])

    def perform_create(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        serializer.save(owner=user, members=[user])


class StudyGroupDetail(generics.RetrieveDestroyAPIView): # groups/<int:pk>/
    # GET get StudyGroup(pk=pk)'s detail
    # DELETE delete StudyGroup(pk=pk) when request.user is owner
      #                               else remove request.user in members
    permission_classes = (IsAuthenticated, IsGroupMember)
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer

    def perform_destroy(self, request, *argc, **kwargs):
        user = StudyUser.objects.get(user=self.request.user)
        studygroup = StudyGroup.objects.get(pk=self.kwargs['pk'])
        attendances = Attendance.objects.all()
        if studygroup.owner == user:
            studygroup.delete()
            for attendance in attendances:
                if attendance.meeting.group == studygroup:
                    attendance.delete()
        else:
            studygroup.members.remove(user)
            for attendance in attendances:
                if attendance.user == user:
                    attendance.delete()


class JoinStudyGroup(APIView): # join_group/?token=<token>
    # GET add user in StudyGroup(pk=f(token)).members
    def get(self, request, format=None):
        token = self.request.query_params.get('token', None)
        if token is None:
            raise Http404
        pk = token # Need to do something more
        if not StudyGroup.objects.filter(pk=pk).exists():
            raise Http404
        studygroup = StudyGroup.objects.get(pk=pk)
        if not studygroup.is_open:
            raise Http404
        user = StudyUser.objects.get(user=request.user)
        studygroup.members.add(user)
        studygroup.save()
        studygroups = StudyGroup.objects.filter(members__in=[user])
        serializer = StudyGroupSerializer(studygroups, many=True)
        return Response(serializer.data)


class OpenCloseStudyGroup(APIView):
    # GET
    def get(self, request, format=None):
        groupId = self.request.query_params.get('groupId', None)
        if not StudyGroup.objects.filter(pk=groupId).exists():
            raise Http404
        studygroup = StudyGroup.objects.get(pk=groupId)
        if studygroup.owner.user != request.user:
            raise Http404
        studygroup.is_open = not studygroup.is_open
        studygroup.save()
        return Response(status=200)

