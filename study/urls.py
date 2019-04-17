from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from study import views
from django.conf.urls import include

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('meetings/', views.MeetingList.as_view()),
    path('meetings/<int:pk>/', views.MeetingDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
