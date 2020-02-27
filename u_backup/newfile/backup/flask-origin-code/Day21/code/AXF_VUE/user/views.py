from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template import loader
from rest_framework.exceptions import APIException, NotAcceptable, ValidationError, AuthenticationFailed, \
    PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from AXF_VUE.settings import USER_TOKEN_TIMEOUT, EMAIL_HOST_USER, SERVER_HOST, ACTIVATE_TIMEOUT
from common.token_generate import generate_token
from user.models import UserModel
from user.serializers import UserSerializer
from user.tasks import send_code, send_email_asy


class UsersView(CreateAPIView):

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        action = request.query_params.get("action")

        if action == "activate":
            try:
                token = request.query_params.get("token")
                u_name = cache.get(token)
                if u_name:
                    cache.delete(token)
                user = UserModel.get_user(u_name)
                user.is_active = True
                user.save()
                # request.session["info"] = "激活成功"
                messages.warning(request._request, "激活成功")
            except Exception as e:
                print(e)
                # request.session["info"] = "激活失败"
                messages.warning(request._request, "激活失败")
            return redirect("/index/")

    def post(self, request, *args, **kwargs):
        action = request.query_params.get("action")

        if action == "register":
            return self.do_register(request, *args, **kwargs)
        elif action == "login":
            return self.do_login(request, *args, **kwargs)
        elif action == "check_username":
            return self.check_user_name(request, *args, **kwargs)
        elif action == "check_email":
            pass
        elif action == "modify_info":
            pass
        elif action == "modify_icon":
            pass
        elif action == "get_info":
            pass
        elif action == "test_asy":
            send_code.delay()
            return Response({"msg": "发送成功"})
        else:
            raise NotAcceptable(detail="请提供正确的动作")

    def do_register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        u_email = serializer.data.get("u_email")
        u_name = serializer.data.get("u_name")

        subject = "AXF用户激活邮件"

        activate_email = loader.get_template("activate.html")

        token = generate_token()

        cache.set(str(token), u_name, timeout=ACTIVATE_TIMEOUT)

        activate_url = SERVER_HOST + "/users/?action=activate&token=" + token
        html_msg = activate_email.render({"u_name": u_name, "activate_url": activate_url})

        send_email_asy.delay(u_email, subject, html_msg)

        data = {
            "msg": "创建成功",
            "status": HTTP_201_CREATED,
            "data": serializer.data
        }

        return Response(data, HTTP_201_CREATED, headers=headers)

    def do_login(self, request, *args, **kwargs):
        u_user = request.data.get("u_user")
        u_password = request.data.get("u_password")

        user = UserModel.get_user(u_user)

        if not user.check_password(u_password):
            raise AuthenticationFailed(detail="密码错误")

        if not user.is_active:
            raise PermissionDenied(detail="用户未激活")

        token = generate_token()

        cache.set(token, user, timeout=USER_TOKEN_TIMEOUT)

        data = {
            "msg": "登录成功",
            "status": HTTP_200_OK,
            "data": {
                "token": token
            }
        }
        return Response(data)

    def check_user_name(self, request, *args, **kwargs):

        u_name = request.data.get("u_name")

        if UserModel.check_username(u_name):
            raise ValidationError(detail="用户名已存在")

        data = {
            "status": HTTP_200_OK,
            "msg": "用户名可用"
        }

        return Response(data)
