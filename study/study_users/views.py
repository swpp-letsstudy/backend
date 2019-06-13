from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import StudyUser
from .serializers import StudyUserSerializer


class StudyUserView(APIView): # user_setting/
    # GET get request.user's StudyUser return { { username, password }, nickname }
    def get(self, request, format=None):
        studyuser = StudyUser.objects.get(user=request.user)
        serializer = StudyUserSerializer(studyuser)
        return Response(serializer.data)

    # PUT { { username, password }, nickname }, update request.user's StudyUser and return updated 
    def put(self, request, format=None):
        if not 'nickname' in request.data.keys():
            raise Http404

        nickname = request.data['nickname']
        
        if StudyUser.objects.filter(nickname=nickname).exists():
            raise Http404

        user = request.user
        studyuser = StudyUser.objects.get(user=user)
        studyuser.nickname = nickname
        studyuser.save()
        return Response(StudyUserSerializer(studyuser).data)
