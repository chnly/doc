import re

from django.contrib.auth.backends import ModelBackend

from users.models import User



def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

def get_user_by_account(account):
    try:
        if re.match(r'1[345789]\d{9}',account):
            user = User.objects.get(mobile = account)
        else:
            user = User.objects.get(username = account)
    except User.DoesNotExist:
        user = None

    return user

class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    重写authenticate方法的思路：
        根据username参数查找用户User对象，username参数可能是用户名，也可能是手机号
        若查找到User对象，调用User对象的check_password方法检查密码是否正确
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user
    '在配置文件中告知Django使用我们自定义的认证后端'