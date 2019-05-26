from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from study.study_users.models import StudyUser


class MyLoginView(ObtainAuthToken): # login/
    # POST { username, password }, login and return { token, username, id }
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        studyuser = StudyUser.objects.get(user=user)
        return Response({
            'token': token.key,
            'nickname': studyuser.nickname,
            'id': user.id,
        })


class MyRegisterView(APIView): # register/
    # POST { username, password }, register
    def post(self, request, format=None):
        if 'username' in request.data.keys() and 'password' in request.data.keys() and 'nickname' in request.data.keys():
            if User.objects.filter(username=request.data['username']).exists():
                return Response('username already exists', status=409)
                
            if StudyUser.objects.filter(nickname=request.data['nickname']).exists():
                return Response('nickname already exists', status=409)

            user = User.objects.create_user(username=self.request.data['username'], password=self.request.data['password'])
            studyuser = StudyUser.objects.get(user=user)
            studyuser.nickname = request.data['nickname']
            studyuser.save()
            return Response('successed', status=201)
        else:
            raise Http404


class MySignOutView(APIView): # signout/
    # POST, signout
    def post(self, request, format=None):
        studyuser = StudyUser.objects.get(user=user)
        studyuser.delete()
        request.user.delete()
