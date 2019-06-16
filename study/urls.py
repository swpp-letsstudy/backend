from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_auth.views import LogoutView

from study.users.views import MyLoginView, MyRegisterView, MySignOutView
from study.study_users.views import StudyUserView
from study.study_groups.views import StudyGroupList, StudyGroupDetail, JoinStudyGroup, OpenCloseStudyGroup
from study.study_group_notices.views import StudyGroupNoticeList, StudyGroupNoticeDetail
from study.study_meetings.views import StudyMeetingList, StudyMeetingDetail
from study.study_meeting_notices.views import StudyMeetingNoticeList, StudyMeetingNoticeDetail
from study.attendances.views import AttendanceView
from study.policies.views import PolicyList, PolicyDetail, MeetingFineList, MeetingFineDetail
from study.cloud_storage.views import CloudStorageFileDetail, CloudStorageFileCreate, CloudStorageFileTree, CloudStorageFileDelete


# Don't need Login
urlpatterns = [
    path('login/', MyLoginView.as_view()),                                  # POST
    path('logout/', LogoutView.as_view()),                                  # POST
    path('register/', MyRegisterView.as_view()),                            # POST
    path('signout/', MySignOutView.as_view()),                              # POST
]

# Need Login (with Auth header)
urlpatterns += [
    path('user_setting/', StudyUserView.as_view()),                         # GET, PUT

    path('groups/', StudyGroupList.as_view()),                              # GET, POST
    path('groups/<int:pk>/', StudyGroupDetail.as_view()),                   # GET, PUT, DELETE
    path('join_group/', JoinStudyGroup.as_view()),                          # GET, ?token=<token>
    path('openclose_group/', OpenCloseStudyGroup.as_view()),                # GET, ?groupId=<groupId>

    path('group_notices/', StudyGroupNoticeList.as_view()),                 # GET, POST ?groupId=<groupId>
    path('group_notices/<int:pk>/', StudyGroupNoticeDetail.as_view()),      # GET, PUT, DELETE ?groupId=<groupId>

    path('meetings/', StudyMeetingList.as_view()),                          # GET, POST ?groupId=<groupId>
    path('meetings/<int:pk>/', StudyMeetingDetail.as_view()),               # GET, PUT, DELETE ?groupId=<groupId>

    path('meeting_notices/', StudyMeetingNoticeList.as_view()),             # GET, POST ?meetingId=<meetingId>
    path('meeting_notices/<int:pk>/', StudyMeetingNoticeDetail.as_view()),  # GET, PUT, DELETE ?meetingId=<meetingId>
    
    path('attendance/', AttendanceView.as_view()),                          # POST
    path('policies/', PolicyList.as_view()),                                # GET, POST ?groupId=<groupId>
    path('policies/<int:pk>/', PolicyDetail.as_view()),                     # GET, PUT, DELETE ?groupId=<groupId>
    path('meeting_fines/', MeetingFineList.as_view()),                      # GET, POST ?meetingId=<meetingId>
    path('meeting_fines/<int:pk>/', MeetingFineDetail.as_view()),           # GET, PUT, DELETE ?meetingId=<meetingId>

    path('cloud_storage/', CloudStorageFileTree.as_view()),                 # GET ?groupId=<groupId>
    path('cloud_storage/delete/', CloudStorageFileDelete.as_view()),        # POST
    path('cloud_storage/get_url/get/', CloudStorageFileDetail.as_view()),   # POST
    path('cloud_storage/get_url/upload/', CloudStorageFileCreate.as_view()),# POST
]

urlpatterns = format_suffix_patterns(urlpatterns)
