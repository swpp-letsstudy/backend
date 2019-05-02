from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from study import views
from django.conf.urls import include

urlpatterns = [
    path('study_groups/', views.StudyGroupList.as_view()),
    path('study_groups/<int:pk>/', views.StudyGroupDetail.as_view()),
    path('study_meetings/', views.StudyMeetingList.as_view()),
    path('study_meetings/<int:pk>/', views.StudyMeetingDetail.as_view()),
    path('attendances/', views.AttendanceCreate.as_view()),
    path('register/', views.CreateUser.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
