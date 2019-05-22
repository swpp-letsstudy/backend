from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import StudyGroup
from .serializers import StudyGroupSerializer
from study.permissions import IsMember


class StudyGroupList(generics.ListCreateAPIView): # groups/
    # GET get request.user's StudyGroups
    # POST { name, info }, create request.user's StudyGroup
    serializer_class = StudyGroupSerializer
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated, IsMember)
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
