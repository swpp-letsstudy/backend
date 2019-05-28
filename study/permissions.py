from rest_framework import permissions

from study.study_users.models import StudyUser


class IsGroupMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = StudyUser.objects.get(user=request.user)
        return user in obj.members.all()


class IsMeetingMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = StudyUser.objects.get(user=request.user)
        group = obj.group
        return user in group.members.all()
