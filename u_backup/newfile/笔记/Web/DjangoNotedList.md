## Django静态文件

Django静态文件的引入和Flask不相同，Flask可以用反向解析方法url_for()来定位到静态文件，但是Django必须要将静态文件注册为`STATICURL`才能引入，具体的区别如下列代码

- Flask：

```html
{# Flask中引入/static/js/jquery.js静态文件，反向解析至static，文件名字为static后面的路径 #}
<script type="text/javascript" src="{{ url_for("static", filename="js/jquery.js") }}"></script>
```

- Django：
  - Django中引入静态变量，需要将STATIC_URL注册在setting.py中

```python
#　首先注册static路径，然后用FileSystemFinder来收录static目录下的静态变量
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)
```


  - 在HTML中引入静态变量

```html
{# Django中引入静态变量，需要用到在setting中注册的STATIC_URL来拼接路径 #}
<link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}css/bootstrap-theme.css"/>
```

如果需要在命令行里面载入静态变量，需要在setting.py文件里面追加STATIC_ROOT变量，在命令行中使用`collectstatic`来载入静态变量

```python
# 这里引入了os模块来定位项目地址
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# 引入FileSystemFinder来查找静态文件，运行collectstatic后会自动将每个app的静态文件，拷贝到需要用到的地方，例如，nginx会拷贝到项目根目录以供调用
STATICFILES_FINDERS = (
"django.contrib.staticfiles.finders.FileSystemFinder",
"django.contrib.staticfiles.finders.AppDirectoriesFinder"
)
```





