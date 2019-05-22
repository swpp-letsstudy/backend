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


#################################################################
# Without Login
class MyLoginView(ObtainAuthToken): # login/
    # POST { username, password }, login and return { token, username, id }
    def post(self, request, format=None):
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
#     # POST, logout
#     def post...


class MyRegisterView(APIView): # register/
    # POST { username, password }, register
    def post(self, request, format=None):
        if 'username' in request.data.keys() and 'password' in request.data.keys():
            if User.objects.filter(username=request.data['username']).exists():
                return Response('username already exists', status=409)

            user = User.objects.create_user(username=self.request.data['username'], password=self.request.data['password'])
            if 'info' in request.data.keys():
                studyuser = StudyUser.objects.get(user=user)
                studyuser.info = request.data['info']
                studyuser.save()
            return Response('successed', status=201)
        else:
            raise Http404




#################################
# Need Login (with Auth header) #
#################################

#################################################################
# User
class MySignOutView(APIView): # signout/
    # POST, signout
    def post(self, request, format=None):
        request.user.delete()


class StudyUserSettingView(APIView): # setting/
    # GET get request.user's StudyUserSetting return { [user], info }
    def get(self, request, format=None):
        studyusersetting = StudyUserSetting.objects.get(user=request.user)
        serializer = StudyUserSettingSerializer(studyusersetting)
        return Response(serializer.data)

    # PUT { [user], info }, update request.user's StudyUserSetting and return updated setting
    def put(self, request, format=None):
        studyusersetting = StudyUserSetting.objects.get(user=request.user)
        serializer = StudyUserSettingSerializer(studyusersetting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise Http404




#################################################################
# Group
class StudyGroupList(generics.ListCreateAPIView): # groups/
    # GET get request.user's StudyGroups
    # POST { name, info }, create request.user's StudyGroup
    serializer_class = StudyGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return StudyGroup.objects.filter(members__in=[user])

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, members=[user])


class StudyGroupDetail(generics.RetrieveDestroyAPIView): # groups/<int:pk>/
    # GET get StudyGroup(pk=pk)'s detail
    # PUT update StudyGroup(pk=pk)'s detail
    # DELETE delete StudyGroup(pk=pk) when request.user is owner
      #                               else remove request.user in members
    permission_classes = (permissions.IsAuthenticated, IsMember)
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer

    def perform_destroy(self, request, *argc, **kwargs):
        user = self.request.user
        studygroup = StudyGroup.objects.get(pk=self.kwargs['pk'])
        if studygroup.owner == user:
            studygroup.delete()
        else:
            studygroup.members.remove(user)


class JoinStudyGroup(APIView): # join_group?token=<token>
    # GET add request.user in StudyGroup(pk=f(token)).members
    def get(self, request, format=None):
        token = self.request.query_params.get('token', None)
        if token is None:
            raise Http404
        pk = token # Need to do something more
        studygroup = StudyGroup.objects.get(pk=pk)
        studygroup.members.add(request.user)
        studygroup.save()
        studygroups = StudyGroup.objects.filter(members__in=[request.user])
        serializer = StudyGroupSerializer(studygroups, many=True)
        return Response(serializer.data)


class StudyGroupNoticeList(generics.ListCreateAPIView): # group_notices?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s StudyGroupNotices
    # POST { title, contents } create request.user's StudyGroupNotice
    serializer_class = StudyGroupNoticeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if not self.request.user in group.members.all():
            raise Http404
        return StudyGroupNotice.objects.filter(group=group)

    def perform_create(self, serializer):
        user = self.request.user
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if user in group.members.all():
            serializer.save(writer=user, group=group)
        else:
            raise Http404

class StudyGroupNoticeDetail(generics.RetrieveDestroyAPIView):
    # GET
    # PUT
    # DELETE
    serializer_class = StudyGroupNoticeSerializer
    queryset = StudyGroupNotice.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        notice = StudyGroupNotice.objects.get(pk=self.kwargs['pk'])
        if notice.writer != user:
            raise HTtp404
        serializer = StudyGroupSerializer(notice, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise Http404
        

class StudyGroupFileList(generics.ListCreateAPIView): # group_files?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s file list
    # POST { filepath }
    serializer_class = StudyFileSerializer
    permission_classes = (permissions.IsAuthenticated,)

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


class StudyGroupTestList(generics.ListCreateAPIView): # group_tests?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s file list
    # POST { title }
    serializer_class = StudyTestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if user in group.members.all():
            return StudyTest.objects.filter(group=group)
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


class PolicyList(generics.ListCreateAPIView): # policies?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s Policies
    serializer_class = PolicySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if user in group.members.all():
            return Policy.objects.filter(group=gropup)
        else:
            raise Http404

    def perform_create(self, serializer):
        user = self.request.user
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if user in group.members.all():
            serializer.save(group=group)


class PolicyDetail(generics.RetrieveUpdateDestroyAPIView): # policies/<int:pk>?groupId=<groupId>
    # GET get PolicySerializer(Policy(pk=pk)).data
    # PUT update Policy(pk=pk) with request.data
    # DELETE if user is owner of group of policy, delete
    serializer_class = PolicySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_update(self, serializer):
        user = self.request.user
        policy = Policy.objects.get(pk=self.kwargs['pk'])
        serializer = PolicySerializer(policy, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise Http404

    def perform_destroy(self, request, *argc, **kwargs):
        user = self.request.user
        policy = Policy.objects.get(pk=self.kwargs['pk'])
        if policy.group.owner == user:
            policy.delete()
        else:
            raise Http404



#################################################################
# Meeting
class StudyMeetingList(generics.ListCreateAPIView): # meetings/
    # GET get StudyMeeting
    # POST { time, info }
    serializer_class = StudyMeetingSerializer
    def get_queryset(self):
        user = self.request.user
        groupId = parse_qs(self.request.GET.urlencode())['groupId'][0]
        study_groups = StudyGroup.objects.filter(members__in=[user], id=groupId)
        return StudyMeeting.objects.filter(group__in=study_groups)

    def perform_create(self, serializer):
        user = self.request.user
        group = StudyGroup.objects.filter(id=self.request.data['groupId'])[0]
        serializer.save(group=group, members=[user])


class StudyMeetingDetail(generics.RetrieveUpdateDestroyAPIView): # meetings/<int:pk>
    permission_classes = (permissions.IsAuthenticated, IsMeetingUser)
    queryset = StudyMeeting.objects.all()
    serializer_class = StudyMeetingSerializer


class AttendanceCreate(generics.CreateAPIView): # attendances?meetingId=<meetingId>
    serializer_class = AttendanceSerializer
    '''
    { userId, meetingId } => toggle attendance 
    Toggle attendance with userId and meetingId.
    If an attendance instance exists, delete it.
    otherwise, create an new attendance instance.
    '''
    def perform_create(self, serializer):
        user = User.objects.filter(id=self.request.data['userId'])[0]
        meeting = StudyMeeting.objects.filter(id=self.request.data['meetingId'])[0]
        attendances = Attendance.objects.filter(user=user, meeting=meeting)
        if attendances:
            attendances.delete()
        else:
            serializer.save(meeting=meeting, user=user)


class StudyMeetingFileList(generics.ListCreateAPIView): # meeting_files?meetingId=<meetingId>
    # GET get StudyMeeting(id=meetingId)'s file list
    serializer_class = StudyFileSerializer
    permission_classes = (permissions.IsAuthenticated,)

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


class StudyMeetingTestList(generics.ListCreateAPIView): # meeting_tests?meetingId=<meetingId>
    # GET get StudyMeeting(id=meetingId)'s file list
    serializer_class = StudyTestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        meetingId = self.request.query_params.get('meetingId', None)
        meeting = StudyMeeting.objects.get(id=meetingId)
        if user in meeting.members.all():
            return StudyTest.objects.filter(meeting=meeting)
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



#################################################################
# ETC
class StudyFileDetail(generics.RetrieveUpdateDestroyAPIView): # files/<int:pk>/
    serializer_class = StudyTestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_destroy(self, request, *argc, **kwargs):
        user = self.request.user
        studyfile = StudyFile.objects.get(pk=self.kwargs['pk'])
        if studyfile.owner == user:
            studyfile.delete()
        else:
            raise Http404


class StudyTestDetail(generics.RetrieveUpdateDestroyAPIView): # tests/<int:pk>/
    serializer_class = StudyTestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_destroy(self, request, *argc, **kwargs):
        user = self.request.user
        studytest = StudyTest.objects.get(pk=self.kwargs['pk'])
        if studytest.owner == user:
            studytest.delete()
        else:
            raise Http404
