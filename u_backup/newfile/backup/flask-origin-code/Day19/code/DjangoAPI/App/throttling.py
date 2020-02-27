from rest_framework.throttling import SimpleRateThrottle


class LearnThrottle(SimpleRateThrottle):

    # rate = "20/m"

    # post_rate = "10/m"

    scope = "common"

    def get_cache_key(self, request, view):

        # 缓存标识   视图函数名字   +   ip

        # return view.__name__ + self.get_ident(request)
        # if request.method == "POST":
        #     self.num_requests, self.duration = self.parse_rate(self.post_rate)
        print("get_cache_key")

        return request.method + self.get_ident(request)