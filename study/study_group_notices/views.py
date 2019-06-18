from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from study.study_users.models import StudyUser
from study.study_groups.models import StudyGroup
from .models import StudyGroupNotice
from .serializers import StudyGroupNoticeSerializer
from study.permissions import IsGroupNoticeMember

class StudyGroupNoticeListFew(generics.ListAPIView): # group_notices/?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s StudyGroupNotices
    # POST { title, contents } create request.user's StudyGroupNotice
    serializer_class = StudyGroupNoticeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = StudyUser.objects.get(user=self.request.user)
        groupId = self.request.query_params.get('groupId', None)
        num = self.request.query_params.get('num', None)
        group = StudyGroup.objects.get(id=groupId)
        if not user in group.members.all():
            raise Http404
        studygroups = StudyGroupNotice.objects.filter(group=group)
        try:
            num = int(num)
        except ValueError:
            raise Http404
        if num > int((len(studygroups)+2)/3):
            raise Http404
        few_studygroups = []
        for i in range(min(num*3+3, len(studygroups))-1, num*3-1, -1):
            few_studygroups.append(studygroups[i])
        return few_studygroups


class StudyGroupNoticeList(generics.ListCreateAPIView): # group_notices/?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s StudyGroupNotices
    # POST { title, contents } create request.user's StudyGroupNotice
    serializer_class = StudyGroupNoticeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = StudyUser.objects.get(user=self.request.user)
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
    # DELETE
    serializer_class = StudyGroupNoticeSerializer
    queryset = StudyGroupNotice.objects.all()
    permission_classes = (IsAuthenticated, IsGroupNoticeMember)

    def perform_destroy(self, request, *argc, **kwargs):
        user = StudyUser.objects.get(user=self.request.user)
        group_notice = StudyGroupNotice.objects.get(pk=self.kwargs['pk'])
        if not group_notice.writer == user:
            raise Http404
        group_notice.delete()
