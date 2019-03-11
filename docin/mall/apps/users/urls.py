from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.RegisterUsernameCountAPIView.as_view(), name='usernamecount'),
#/users/auths/
    url(r'^$', views.RejisterCreateUser.as_view(), name='rejisteruser'),
]