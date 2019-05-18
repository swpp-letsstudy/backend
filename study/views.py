from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.parse import parse_qs

from study.serializers import *
from study.permissions import *
from study.models import *

from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class MyLoginView(ObtainAuthToken): # login/
    # POST { username, password }
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'id': user.id,
        })


# class LogoutView:   in rest_auth.views.LogoutView # logout/
#     # POST
#     def post...


class MyRegisterView(APIView): # register/
    # POST { username, password }
    def post(self, request, *args, **kwargs):
        if 'username' in request.data.keys() and 'password' in request.data.keys():
            if User.objects.filter(username=request.data['username']).count() == 0:
                User.objects.create_user(username=self.request.data['username'], password=self.request.data['password'])
                return Response('successed', status=201)
            return Response('username exists', status=409)
        else:
            raise Http404




#################################
# Need Login (with Auth header) #
#################################

class StudyGroupList(generics.ListCreateAPIView): # study_groups/
    # GET, POST { name, info }
    serializer_class = StudyGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return StudyGroup.objects.filter(members__in=[user])

    def perform_create(self, serializer):
        user = self.request.user
        if serializer.is_valid():
            serializer.save(owner=user, members=[user])


class StudyGroupDetail(generics.RetrieveDestroyAPIView): # study_groups/<int:pk>/
    # GET, PUT, DELETE
    permission_classes = (permissions.IsAuthenticated, IsMember)
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer

    def perform_destroy(self, request, *argc, **kwargs):
        pk = self.kwargs.get('pk')
        user = self.request.user
        studygroup = StudyGroup.objects.get(pk=pk)
        if studygroup.owner == user:
            studygroup.delete()
        else:
            studygroup.members.remove(user)
        studygroups = StudyGroup.objects.filter(members__in=[user])
        serializer = StudyGroupSerializer(studygroups, many=True)
        return Response(serializer.data)


class JoinStudyGroup(APIView): # join_study_group?token=<token>
    # GET
    def get(self, request, format=None):
        token = parse_qs(self.request.GET.urlencode())['token'][0]
        pk = token # Need to do something more
        studygroup = StudyGroup.objects.get(pk=pk)
        studygroup.members.add(request.user)
        studygroup.save()
        studygroups = StudyGroup.objects.filter(members__in=[request.user])
        serializer = StudyGroupSerializer(studygroups, many=True)
        return Response(serializer.data)


class StudyUserSettingView(APIView): # user_setting/
    # GET, PUT { [user_setting] }
    def get(self, request, format=None):
        studyusersetting = StudyUserSetting.objects.get(user=request.user)
        serializer = StudyUserSettingSerializer(studyusersetting)
        return Response(serializer.data)

    def put(self, request, format=None):
        studyusersetting = StudyUserSetting.objects.get(user=request.user)
        serializer = StudyUserSettingSerializer(studyusersetting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise Http404


class StudyGroupNoticeList(generics.ListCreateAPIView): # study_notices?groupId=<groupId>
    # GET, POST { title, contents }
    serializer_class = StudyGroupNoticeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        groupId = parse_qs(self.request.GET.urlencode())['groupId'][0]
        group = StudyGroup.objects.get(id=groupId)
        if not self.request.user in group.members.all():
            raise Http404
        return StudyGroupNotice.objects.filter(group=group)

    def perform_create(self, serializer):
        user = self.request.user
        groupId = parse_qs(self.request.GET.urlencode())['groupId'][0]
        group = StudyGroup.objects.get(id=groupId)
        if not user in group.members.all():
            raise Http404
        serializer.save(writer=user, group=group)


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
