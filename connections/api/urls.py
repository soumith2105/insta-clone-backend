from django.urls import path
from .views import (
    FollowingListAPIView,
    FollowersListAPIView,
    ConnectionCreateAPIView,
    ConnectionDeleteAPIView,
    FollowRequestListAPIView,
    FollowRequestAcceptAPIView,
    FollowRequestDeleteAPIView,
)


urlpatterns = [
    path('following/', FollowingListAPIView.as_view(), name='following'),
    path('followers/', FollowersListAPIView.as_view(), name='followers'),
    path('followrequest/', FollowRequestListAPIView.as_view(), name='follow_requests'),
    path('followrequest/<str:slug>/', FollowRequestAcceptAPIView.as_view(), name='follow_requests_accept'),
    path('followrequest/<str:slug>/delete/', FollowRequestDeleteAPIView.as_view(), name='follow_requests_accept'),
    path('follow/', ConnectionCreateAPIView.as_view(), name='follow_create'),
    path('followdelete/<str:slug>/', ConnectionDeleteAPIView.as_view(), name='follow_delete'),
]