from time import sleep
from loguru import logger
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler


class IndexHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        # print(self)
        hobbies = ["learn", 'study']
        http_client = AsyncHTTPClient()
        # response = yield [http_client.fetch("http://cn.bing.com")]
        # print(f'response ::: ', response)
        # response_dict = yield dict(response2=http_client.fetch("http://baidu.com"))
        # print(f'response_dict :::', response_dict)
        # response2 = response_dict["response2"]
        logger.info(self.__dict__)
        logger.info(dir(self))
        # self.write("<h1>this is a test for render</h1>")
        # self.render("index.html", title='test', hobbies=hobbies)
        # sleep(5)
        # self.redirect(url='http://cn.bing.com')
        # print("this is a test of gen")
        self.write({"msg": "ok"})
        return


class DateHandler(RequestHandler):
    def get(self, year, month, day):
        print(year, month, day)
        self.write("Date")


@gen.coroutine
def test_gen():
    return "oops"


