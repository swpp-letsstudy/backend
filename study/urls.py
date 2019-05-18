from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

from rest_auth.views import LogoutView
from study.views import *

# Don't need Login
urlpatterns = [
    path('login/', MyLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', MyRegisterView.as_view()),
]

# Need Login (with Auth header)
urlpatterns += [
    path('study_groups/', StudyGroupList.as_view()),                # GET, POST
    path('study_groups/<int:pk>/', StudyGroupDetail.as_view()),     # GET, PUT, DELETE
    path('join_study_group/', JoinStudyGroup.as_view()),            # GET
    path('user_setting/', StudyUserSettingView.as_view()),          # GET, PUT
    path('study_notices/', StudyGroupNoticeList.as_view()),         # GET, POST
    path('study_meetings/', StudyMeetingList.as_view()),            # GET, POST
    path('study_meetings/<int:pk>/', StudyMeetingDetail.as_view()), # GET, PUT, DELETE
    path('attendances/', AttendanceCreate.as_view()),               # POST
]

urlpatterns = format_suffix_patterns(urlpatterns)
