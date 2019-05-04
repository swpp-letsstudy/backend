from rest_framework import generics
from study.serializers import *
from study.permissions import *
from study.models import *
from urllib.parse import parse_qs
from django.contrib.auth.models import User

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class StudyGroupList(generics.ListCreateAPIView):
    serializer_class = StudyGroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsUserInStudyGroup)

    def get_queryset(self):
        user = self.request.user
        return StudyGroup.objects.filter(members__in=[user])

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, members=[user])


class StudyGroupDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsMember)
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer


class JoinStudyGroup(APIView):
    def get(self, request, pk, format=None):
        studygroup = StudyGroup.objects.get(pk=pk)
        studygroup.members.add(request.user)
        serializer = StudyGroupSerializer(studygroup, data=studygroup)
        serializer.is_valid()
        print("serializer.data: " + str(serializer.data))
        serializer.save()
        return Response(data=serializer.data)


class StudyMeetingList(generics.ListCreateAPIView):
    serializer_class = StudyMeetingSerializer

    def get_queryset(self):
        user = self.request.user
        groupId = parse_qs(self.request.GET.urlencode())['groupId'][0]
        study_groups = StudyGroup.objects.filter(members__in=[user], id=groupId)
        return StudyMeeting.objects.filter(group__in=study_groups)

    def perform_create(self, serializer):
        group = StudyGroup.objects.filter(id=self.request.data['groupId'])[0]
        serializer.save(group=group)


class StudyMeetingDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsMeetingUser)
    queryset = StudyMeeting.objects.all()
    serializer_class = StudyMeetingSerializer


class AttendanceCreate(generics.CreateAPIView):
    serializer_class = AttendanceSerializer

    '''
    { userId, meetingId } => toggle attendance 
    Toggle attendance with userId and meetingId.
    If an attendance instance exists, delete it.
    otherwise, create an new attendance instance.
    '''
    def perform_create(self, serializer):
        user=User.objects.filter(id=self.request.data['userId'])[0]
        meeting = StudyMeeting.objects.filter(id=self.request.data['meetingId'])[0]
        attendances = Attendance.objects.filter(user=user, meeting=meeting)
        if attendances:
            attendances.delete()
        else:
            serializer.save(meeting=meeting, user=user)
