from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LearnMiddleware(MiddlewareMixin):

    def process_request(self, request):

        print(request.path)
        # 实现功能
        """
        
            记录，日志
            用户认证
            黑名单，白名单
            优先级
            拦截器，反爬虫
                - 三十秒一次
                - 一分钟之内最多十次
                - 数据正确给你错误状态码
                - 加密
                - 动态加密
        
        """

    def process_exception(self, request, exception):
        print(request, exception)

        return redirect(reverse("app:index"))