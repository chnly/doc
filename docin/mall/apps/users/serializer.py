from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import User
from django_redis import get_redis_connection
import re

class RegisterCreateSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(label='校验密码', allow_null=False,    allow_blank=False,  write_only=True)
    sms_code = serializers.CharField(label='短信验证码', max_length=6,min_length=6,allow_null=False, allow_blank=False,  write_only=True)
    allow = serializers.CharField(label='是否同意协议',   allow_null=False,   allow_blank=False,  write_only=True)
    token = serializers.CharField(label='登录状态token', read_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2', 'sms_code', 'id', 'username', 'allow', 'mobile', 'token']
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, value):

        if not re.match(r'^1[345789]\d{9}', value):
            raise serializers.ValidationError('手机号格式不正确')
        return value

    def validate_allow(self, value):

        if not value:
            raise serializers.ValidationError('您未同意协议')
        return value

    def validate(self, attrs):

        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError('密码不一致')

        redis_conn = get_redis_connection('code')
        mobile = attrs['mobile']
        code = attrs['sms_code']
        redis_code = redis_conn.get('sms_' + mobile)
        if redis_code is None:
            raise serializers.ValidationError('验证码已过期')
        if code != redis_code.decode():
            raise serializers.ValidationError('验证码不正确')

        return attrs

    def create(self, validated_data):

        # 删除多余字段
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        user = super().create(validated_data)

        # 修改密码
        user.set_password(validated_data['password'])
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
   用户详细信息序列化器
   """
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')
