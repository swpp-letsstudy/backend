from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from study.study_users.models import StudyUser
from study.study_groups.models import StudyGroup
from .models import StudyGroupNotice
from .serializers import StudyGroupNoticeSerializer


class StudyGroupNoticeList(generics.ListCreateAPIView): # group_notices/?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s StudyGroupNotices
    # POST { title, contents } create request.user's StudyGroupNotice
    serializer_class = StudyGroupNoticeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = StudyUser.objects.get(user=request.user)
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if not user in group.members.all():
            raise Http404
        return StudyGroupNotice.objects.filter(group=group)

    def perform_create(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        groupId = self.request.query_params.get('groupId', None)
        group = StudyGroup.objects.get(id=groupId)
        if not user in group.members.all():
            raise Http404
        serializer.save(writer=user, group=group)


class StudyGroupNoticeDetail(generics.RetrieveDestroyAPIView): # group_notices/<int:pk>/?groupId=<groupId>
    # GET
    # PUT
    # DELETE
    serializer_class = StudyGroupNoticeSerializer
    queryset = StudyGroupNotice.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        user = StudyUser.objects.get(user=self.request.user)
        group_notice = StudyGroupNotice.objects.get(pk=self.kwargs['pk'])
        if group_notice.writer != user:
            raise Http404
        serializer = StudyGroupNoticeSerializer(group_notice, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise Http404

    def perform_destroy(self, request, *argc, **kwargs):
        user = StudyUser.objects.get(user=self.request.user)
        group_notice = StudyGroupNotice.objects.get(pk=self.kwargs['pk'])
        if not group_notice.writer == user:
            raise Http404
        group_notice.delete()
