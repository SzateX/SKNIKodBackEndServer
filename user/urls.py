from django.urls import re_path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from user.views import UserViewSetList, UserViewSetDetail, GroupViewSetList, GroupViewSetDetail

urlpatterns = [
    re_path(r'^api-auth/',
            include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^rest-auth/', include('dj_rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^obtain-token/', TokenObtainPairView.as_view(),
            name='token_obtain_pair'),
    re_path(r'^verify-token/', TokenVerifyView.as_view(), name='token_verify'),
    re_path(r'^api/users/$', UserViewSetList.as_view(), name='user_list'),
    re_path(r'^api/users/(?P<pk>\d+)/$', UserViewSetDetail.as_view(), name='user_detail'),
    re_path(r'^api/groups/$', GroupViewSetList.as_view(), name='group_list'),
    re_path(r'^api/groups/(?P<pk>\d+)/$', GroupViewSetDetail.as_view(), name='group_detail'),
]