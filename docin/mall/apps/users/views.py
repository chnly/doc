from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RegisterCreateSerializer, UserDetailSerializer
from .models import User

class RegisterUsernameCountAPIView(APIView):
    """
    获取用户名的个数
    GET:  /users/usernames/(?P<username>\w{5,20})/count/
    """
    def get(self, request, username):
        # 通过模型查询,获取用户名个数
        count = User.objects.filter(username = username).count()
        #组织数据
        context = {
            'count': count,
            'username': username
        }
        return Response(context)


class RejisterCreateUser(CreateAPIView):

    serializer_class = RegisterCreateSerializer


class UserDetailView(RetrieveAPIView):
    """
   获取登录用户的信息
   GET /users/
   既然是登录用户,我们就要用到权限管理
   在类视图对象中也保存了请求对象request
   request对象的user属性是通过认证检验之后的请求用户对象
   """
    permission_classes = [IsAuthenticated]

    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user