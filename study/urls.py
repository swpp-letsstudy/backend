from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from study import views
from django.conf.urls import include

urlpatterns = [
    path('studygroups/', views.StudyGroupList.as_view()),
    path('studymeetings/', views.StudyMeetingList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
