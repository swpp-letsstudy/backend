from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_auth.views import LogoutView

from study.users.views import MyLoginView, MyRegisterView, MySignOutView
from study.study_user_settings.views import StudyUserSettingView
from study.study_groups.views import StudyGroupList, StudyGroupDetail, JoinStudyGroup
from study.study_group_notices.views import StudyGroupNoticeList, StudyGroupNoticeDetail
from study.study_files.views import StudyGroupFileList, StudyMeetingFileList, StudyFileDetail
from study.study_tests.views import StudyGroupTestList, StudyMeetingTestList, StudyTestDetail
from study.policies.views import PolicyList, PolicyDetail
from study.study_meetings.views import StudyMeetingList, StudyMeetingDetail
from study.attendances.views import AttendanceCreate


# Don't need Login
urlpatterns = [
    path('login/', MyLoginView.as_view()),                      # POST
    path('logout/', LogoutView.as_view()),                      # POST
    path('register/', MyRegisterView.as_view()),                # POST
    path('signout/', MySignOutView.as_view()),                  # POST
]

# Need Login (with Auth header)
urlpatterns += [
    path('setting/', StudyUserSettingView.as_view()),                   # GET, PUT

    path('groups/', StudyGroupList.as_view()),                          # GET, POST
    path('groups/<int:pk>/', StudyGroupDetail.as_view()),               # GET, PUT, DELETE
    path('join_group/', JoinStudyGroup.as_view()),                      # GET
    path('group_notices/', StudyGroupNoticeList.as_view()),             # GET, POST
    path('group_notices/<int:pk>/', StudyGroupNoticeDetail.as_view()),  # GET, POST
    path('group_files/', StudyGroupFileList.as_view()),                 # GET, POST
    path('group_tests/', StudyGroupTestList.as_view()),                 # 
    path('policies/', PolicyList.as_view()),                            # 
    path('policies/<int:pk>/', PolicyDetail.as_view()),                 # 

    path('meetings/', StudyMeetingList.as_view()),                      # GET, POST
    path('meetings/<int:pk>/', StudyMeetingDetail.as_view()),           # GET, PUT, DELETE
    path('attendances/', AttendanceCreate.as_view()),                   # POST
    path('meeting_files/', StudyMeetingFileList.as_view()),             # 
    path('meeting_tests/', StudyMeetingTestList.as_view()),             # 

    path('files/<int:pk>/', StudyFileDetail.as_view()),                 # 
    path('tests/<int:pk>/', StudyTestDetail.as_view()),                 # 
]

urlpatterns = format_suffix_patterns(urlpatterns)
