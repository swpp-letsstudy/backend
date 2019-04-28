from rest_framework import permissions
from urllib.parse import parse_qs

from study.models import StudyGroup


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True if obj.users.filter(id=request.user.id) else False


class IsGroupOwnerOrMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.owner == user or obj.members.filter(id=user.id).exists()


class IsMeetingUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        group = obj.group
        return group.owner == user or group.members.filter(id=user.id).exists()