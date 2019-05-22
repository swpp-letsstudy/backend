from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from .serializers import PolicySerializer
from .models import Policy
from study.study_groups.models import StudyGroup


class PolicyList(generics.ListCreateAPIView): # policies?groupId=<groupId>
    # GET get StudyGroup(id=groupId)'s Policies
    serializer_class = PolicySerializer
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

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
