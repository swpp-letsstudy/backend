from rest_framework import permissions

from study.study_users.models import StudyUser

class IsGroupNoticeMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = StudyUser.objects.get(user=request.user)
        return user in obj.group.members.all()


class IsMeetingNoticeMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = StudyUser.objects.get(user=request.user)
        return user in obj.meeting.group.members.all()


class IsGroupMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = StudyUser.objects.get(user=request.user)
        return user in obj.members.all()


class IsMeetingMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = StudyUser.objects.get(user=request.user)
        group = obj.group
        return user in group.members.all()
