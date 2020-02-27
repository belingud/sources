官网对inspect模块的解释是：
inspect模块主要提供了四种用处：

对是否是模块，框架，函数等进行类型检查
获取源码
获取类或函数的参数信息
解析堆栈
说白了就是以下三大类：

检查对象(isxxx)
获取对象（getxxx)
解析堆栈对象实例
先说说解析堆栈对象实例，个人感觉这是最有用的
我们可以写个Demo来模拟log日志打印
我们希望打印的时候实现以下需求：

打印变量值，也打印变量名
打印出是在哪个文件，哪个方法，哪一行执行打印了
import inspect

def f2():
    print(inspect.stack())

def f1():
    f2()

def main():
    f1()

if __name__ == "__main__":
    main()

打印结果简化后是这样的：

[
FrameInfo(frame=<frame object at F398>, filename='D:/demo.py', lineno=5, function='v2', code_context=['print(inspect.stack())\n'], index=0),
FrameInfo(frame=<frame object at 1BA8>, filename='D:/demo.py', lineno=9, function='v1', code_context=['v2()\n'], index=0),
FrameInfo(frame=<frame object at 1A08>, filename='D:/demo.py', lineno=13, function='main', code_context=['v1()\n'], index=0),
FrameInfo(frame=<frame object at F1F0>, filename='D:/demo.py', lineno=17, function='<module>', code_context=['main()\n'], index=0)
]

于是我们可以知道返回堆栈的返回结果是几个元组组成的列表。
我们的代码调用关系是：__main__–> main()–>f1()–> f2()
仔细看打印信息，我们可以发现：
列表中的第0个元组是f2()的堆栈信息
列表中的第1个元组是f1()的堆栈信息
列表中的第2个元组是main()的堆栈信息
列表中的第3个元组是__main__的堆栈信息

层层调用，层层递归，最终指向最初调用的位置，
有没有发现它和Python报错信息非常相像，我们确实可以用inspect模拟logger日志，OK来个实例吧：

import inspect
import re
import time
import json

class Person:
    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city

    def toJSON(self):
        return {"name": self.name, "age": self.age, "city": self.city}

def wdp(_variable):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # 堆栈的最里层是该打印函数,获取上一层的调用故取第二层堆栈
    exec_info = inspect.stack()[1]
    # 当前执行的文件名
    fn = exec_info[1].rsplit("/", 1)[1]

    # 所在行
    _line = exec_info[2]
    # 调用的方法
    _function = exec_info[3]
    
    # 执行的命令
    _cmd = exec_info[4][0]
    
    # 执行的命令中参数的名称
    pattern = re.compile(
        wdp.__name__ + '\((.*?)\)$',
        re.S
    )
    _cmd = _cmd.strip().replace('\r', '').replace('\n', '')
    # 变量名
    vn = re.findall(pattern, _cmd.strip())[0]
    
    # 变量转字符串
    if hasattr(_variable, "toJSON"):
        info = json.dumps(_variable.toJSON(), ensure_ascii=False)
    elif hasattr(_variable, "__str__"):
        info = _variable.__str__()
    else:
        info = str(_variable)
    log_info = '[{time}] [{filename}] [{func}] [{line}] {variable_name} = {variable}'.format(
        time=t,
        filename=fn,
        func=_function,
        line=_line,
        variable_name=vn,
        variable=info
    )
    print(log_info)

if __name__ == '__main__':
    p = Person("王宝强", 25, "上海")
    wdp(p)

最后再说说检查对象和获取对象

一个Python脚本中对象无外乎以下几种：

模块
类
方法
变量（信息太少，inspect直接忽略了）
于是上面的三大类又可以细分为：

检查对象
检查是否为模块（ ismodule）
检查是否为类（）
是否为类（ isclass）
是否为基类（ isabstract）
检查是否为方法（）
是否为方法（ ismethod）
是否为函数（ isfunction）
是否为生成器函数（ isgeneratorfunction）
是否为生成器（ isgenerator）
是否为traceback（ istraceback）
是否为built-in函数或方法（ isbuiltin）
是否为用户自定义或者built-in方法（ isroutine）
是否为方法标识（ismethoddescriptor）
检查是否为变量（）
是否为数字标识符
获取对象（getxxx)
获取模块（）
获取模块（ getmodule）
获取模块名（ getmodulename）
获取类（ ）
获取类的继承结构（ getmro）
获取方法声明的参数（ getargspec）
获取方法（）
获取方法声明的参数（ getargspec）
获取方法声明的值（ getargvalues）
模块/类/方法都有的：
获取成员（ getmembers）
获取源码（ getsource）
获取源码所在行（ getsourcelines）
获取对象定义所在的模块的文件名 （ getfile）
获取对象注释（ getcomments）
获取 对象documentation信息（ getdoc）