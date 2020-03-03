from tornado import ioloop, options
import tornado
from tornado.options import define, options, parse_command_line

from TornadoProject import create_app

# 定义
define(name="port", default="8888", help="port default 8888")

if __name__ == '__main__':

    app = create_app()
    # 转换命令行参数
    parse_command_line()
    # 选项调用
    app.listen(options.port)
    print(options.as_dict())
    tornado.ioloop.IOLoop.current().start()
