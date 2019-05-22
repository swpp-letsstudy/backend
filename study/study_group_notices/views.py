from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from .serializers import StudyGroupNoticeSerializer
from .models import StudyGroupNotice
from study.study_groups.models import StudyGroup
from study.study_groups.serializers import StudyGroupSerializer


class StudyGroupNoticeList(generics.ListCreateAPIView): # group_notices?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s StudyGroupNotices
    # POST { title, contents } create request.user's StudyGroupNotice
    serializer_class = StudyGroupNoticeSerializer
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        notice = StudyGroupNotice.objects.get(pk=self.kwargs['pk'])
        if notice.writer != user:
            raise Http404
        serializer = StudyGroupSerializer(notice, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise Http404
