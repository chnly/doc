from random import randint

from rest_framework.response import Response

from libs.yuntongxun.sms import CCP
from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from .serializer import RegisterSMSCodeSerializer

class RegisterImageAPIView(APIView):
    '''
    1.接收 image_code_id
    2.生成图片和验证码
    3.把验证码保存到redis中
    4.返回图片相应

    GET         /verifications/imagecodes/(?P<image_code_id>.+)/

    GET         /verifications/imagecodes/?image_code_id=xxxxxx
    '''
    def get(self,request,image_code_id):
        #1.接收image_code_id
        # 2.生成图片和验证码
        text, image = captcha.generate_captcha()
        # 3.把验证码保存到redis中
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_' + image_code_id, 60, text)
        # 4.返回图片相应
        return HttpResponse(image, content_type='image/jpeg')


class RegisterSmscodeAPIView(APIView):

    def get(self,request,mobile):
        # 1.接收参数
        params = request.query_params
        # 2.校验参数
        serializer = RegisterSMSCodeSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        # 3.生成短信
        sms_code = '%06d'%randint(0,999999)
        # 4.将短信保存在redis中
        redis_conn = get_redis_connection('code')
        redis_conn.setex('sms_%s'+ mobile, 5*60 ,sms_code)
        # 5.使用云通讯发送短信
        # ccp = CCP()
        # ccp.send_template_sms(mobile,[sms_code,5],1)
        from celery_tasks.sms.tasks import send_sms_code
        # delay 的参数和 任务的参数对应
        # 必须调用 delay 方法,才能执行celery
        send_sms_code.delay(mobile, sms_code)
        # 6.返回相应
        return Response({'message':'ok'})