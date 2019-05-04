from rest_framework import permissions
from urllib.parse import parse_qs

from study.models import StudyGroup


class IsUserInStudyGroup(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True if obj.users.filter(id=request.user.id) else False


class IsMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.members.filter(id=user.id).exists()


class IsRightToken(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True


class IsMeetingUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        group = obj.group
        return group.owner == user or group.members.filter(id=user.id).exists()