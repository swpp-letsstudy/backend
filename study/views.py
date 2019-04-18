from rest_framework import generics, permissions
from django.contrib.auth.models import User

from study.models import *
from study.serializers import *
from study.permissions import *

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class StudyGroupList(generics.ListAPIView):
    serializer_class = StudyGroupSerializer

    def get_queryset(self):
        user = self.request.user
        ret = StudyGroup.objects.filter(users__in=[user])
        print(ret)
        return ret

class StudyMeetingList(generics.ListAPIView):
    queryset = StudyMeeting.objects.all()
    serializer_class = StudyMeetingSerializer
