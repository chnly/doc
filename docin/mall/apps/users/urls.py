from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.RegisterUsernameCountAPIView.as_view(), name='usernamecount'),
#/users/auths/
    url(r'^$', views.RejisterCreateUser.as_view(), name='rejisteruser'),
    url(r'^infos/$',views.UserDetailView.as_view(),name='detail'),
    #Django REST framework JWT提供了登录获取token的视图，可以直接使用, 在users应用中的urls添加路由信息
    url(r'auths/', obtain_jwt_token, name='auths'),
]