from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

from rest_auth.views import LogoutView
from study.views import *

urlpatterns = [
    path('study_groups/', StudyGroupList.as_view()),
    path('study_groups/<int:pk>/', StudyGroupDetail.as_view()),
    path('join_study_group/<int:pk>/', JoinStudyGroup.as_view()),
    path('exit_study_group/<int:pk>/', ExitStudyGroup.as_view()),
    path('study_meetings/', StudyMeetingList.as_view()),
    path('study_meetings/<int:pk>/', StudyMeetingDetail.as_view()),
    path('attendances/', AttendanceCreate.as_view()),
]

urlpatterns += [
    path('login/', MyLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', MyRegisterView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
