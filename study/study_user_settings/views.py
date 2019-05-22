from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from study.study_user_settings.models import StudyUserSetting
from study.study_user_settings.serializers import StudyUserSettingSerializer


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
