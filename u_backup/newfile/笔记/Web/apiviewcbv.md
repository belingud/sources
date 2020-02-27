1.APIView
DRF框架的视图的基类是 APIView
APIView的基本使用和View类似

Django默认的View请求对象是 HttpRequest，REST framework 的请求对象是 Request。
Request对象的数据是自动根据前端发送数据的格式进行解析之后的结果。
HttpRequest.GET ————> Request.query_params
HttpRequest.POST 、HttpRequest.body————> Request.data

Django默认的View响应对象是 HttpResponse(以及子类),REST framework 的响应对象是Response。
构造方式：
Response(data, status=None, template_name=None, headers=None, content_type=None)
参数说明：

List item

data: 为响应准备的序列化处理后的数据；

status: 状态码，默认200；

template_name: 模板名称，如果使用HTMLRenderer时需指明；

headers: 用于存放响应头信息的字典；

content_type: 响应数据的Content-Type，通常此参数无需传递，REST framework会根据前端所需类型数据来设置该参数。

支持定义的属性：
authentication_classes列表或元祖，身份认证类
permissoin_classes列表或元祖，权限检查类
throttle_classes列表或元祖，流量控制类。

在APIView中仍以常规的类视图定义方法来实现get() 、post() 或者其他请求方式的方法。如下：


```python
''' serializers.py '''

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookInfo    # 设置关联模型     model就是关联模型
        fields = '__all__'  # fields设置字段   __all__表示所有字段
        
'''urls.py'''
url(r'^center/$',views.CenterView.as_view())
```



```python
''' views.py '''
class CenterView(APIView):

    def get(self,request):

        #  以前的 HttpRequest.GET  
        #  现在的
        # /center/?a=100&b=python
        params = request.query_params
        print(params)

        # 响应不同的第一个
        dict = {
            'name':'hello'
        }
        # return JsonResponse(dict)

        return Response(dict)

        # return HttpResponse('get')

    def post(self,request):

        # 以前的 HttpRequest.POST,HttpRequest.body
        # 现在
        # form 表单提交数据
        data = request.data
        print(data)
        
        return HttpResponse('post')
```




2.实例：使用APIView实现列表功能

```python
'''urls.py'''
url(r'^books/$',views.BookListAPIView.as_view())

'''views.py'''

class BookListAPIView(APIView):
    '''书籍列表页'''
    def get(self,request):
        # 1.获取所有书籍
        books = BookInfo.objects.all()
        # 2.通过序列化器的转换（模型转换为JSON）
        serializer = BookSerializer(book,many=True)
        # 3.返回响应
        return Response(serializer.data)

    def post(self,request):

        # 1.接收参数
        data = request.data
        # 2.验证参数（序列化器的校验）
        serializer = BookSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # 3.数据入库
        serializer.save()
        # 4.返回响应
        return Response(serializer.data)
```


3.GenericAPIView
GenericAPIView是继承自APIView，GenericAPIView肯定在APIView的基础上 封装了一些属性和方法：增加了对于列表视图和详情视图可能用到的通用方法和属性的支持

属性：
queryset 设置结果集
serializer_class 设置序列化器
lookup_field 查询指定的对象

方法：
get_queryset(self) 返回视图使用的查询集
get_serializer(self,_args, *_kwargs) 返回序列化器对象
get_object(self) 返回详情视图所需的模型类数据对象

通常使用时，可搭配一个或多个扩展类（Mixin类，详见4.）


```python
##########GenericAPIView列表视图##################

'''urls.py'''
url(r'^books/$',views.BookListGenericAPIView.as_view())
```



```python
'''views.py'''

class BookListGenericAPIView(GenericAPIView):
    
    '''列表视图'''

    # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器类
    serializer_class = BookSerializer

    def get(self,request):

        # 1.获取所有书籍
        # books = BookInfo.objects.all()
        # 上面写法也可以，但属性就白白浪费了，没有充分发挥属性的作用

        books = self.get_queryset()

        # 2.创建序列化器
        # serializer = BookSerializer(books,many=True)
        # 以上写法也可可以，但是还是没有发挥属性的作用

        # get_serializer()相当于BookSerializer()
        serializer = self.get_serializer(book,many=True)

        # 3.返回响应
        return Response(serializer.data)
```


​            
```python
    def post(self,request):

        # 1.获取参数
        data = request.data
        # 2.创建序列化器
        serializer = self.get_serializer(data=data)
        # 3.校验
        serializer.is_valid(raise_exception=True)
        # 4.保存
        serializer.save()
        # 5.返回响应
        return Response(serializer.data)

class BookDetailGenericAPIView(GenericAPIView):

    '''详情视图'''

    # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器类
    serializer_class = BookSerializer

    # 默认是pk   修改后以下参数都要变
    lookup_field = 'id'

    def get(self,request,id):

        # 1.获取对象
        book = self.get_object()
        # 2.创建序列化器
        serializer = self.get_serializer(book)
        # 3.返回响应
        return Response(serializer.data)
```


```python
    def put(self,request,id):

        # 1.获取对象
        book = self.get_object()
        # 2.接收参数
        data = request.data
        # 3.创建序列化器
        serializer = self.get_serializer(instance=book,data=data)
        # 4.验证
        serializer.is_valid(raise_exception=True)
        # 5.保存（更新）
        serializer.save()
        # 3.返回响应
        return Response(serializer.data)
```



```python
    def delete(self,request,pk):
        # 1.获取对象
        book = self.get_object()
        # 2.删除
        book.delete()
        # 3.返回响应
        return Response(status=status.HTTP_204_NO_CONTENT)
```


4.GenericAPIView和Mixin配合使用
mixin类提供用于提供基本视图行为的操作。请注意，mixin类提供了操作方法，而不是直接定义处理程序方法，例如.get()和.post()。这允许更灵活的行为组合。

ListModelMixin
提供一种.list(request, *args, **kwargs)实现列出查询集的方法。
CreateModelMixin
提供.create(request, *args, **kwargs)实现创建和保存新模型实例的方法。
RetrieveModelMixin
提供一种.retrieve(request, *args, **kwargs)方法
UpdateModelMixin
提供.update(request, *args, **kwargs)实现更新和保存现有模型实例的方法。
DestroyModelMixin
提供一种.destroy(request, *args, **kwargs)实现删除现有模型实例的方法。

```python
'''urls.py'''
```
 	url(r'^booklist/$',views.BookListGenericMixinAPIView.as_view())


```python
'''views.py'''

# ListModelMixin        获取全部对象（列表）
# CreateModelMixin      新增资源
# RetrieveModelMixin    获取一个资源
# UpdateModelMixin      更新一个资源
# DestoryModelMixin     删除一个资源

class BookListGenericMixinAPIView(ListModelMixin,CreateModelMixin,GenericAPIView):

   # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器类
    serializer_class = BookSerializer

    def get(self,request):

        return self.list(request)

    def post(self,request):

        return self.create(request)

    def post(self,request):

        return self.create(request)
    
class BookDetailGenericMixinAPIView(R,U,D):

    def get(self,request):

        return self.retrieve(request)

    def put(self,request):

        return self.update(request)

    def delete(self,request):

        return self.destroy(request)
```


6.三级视图
CreateAPIView
提供post方法处理程序。

ListAPIView
用于只读端点以表示模型实例的集合。
提供get方法处理程序。

RetrieveAPIView
用于表示单个模型实例的只读端点。
提供get方法处理程序。

DestroyAPIView
用于单个模型实例的仅删除端点。
提供delete方法处理程序。

UpdateAPIView
用于单个模型实例的仅更新端点。
提供put和patch方法处理程序。

ListCreateAPIView
用于读写端点以表示模型实例的集合。
提供get和post方法处理程序。

RetrieveUpdateAPIView
用于读取或更新端点以表示单个模型实例。
提供get，put并且patch方法处理。

RetrieveDestroyAPIView
用于读取或删除端点以表示单个模型实例。
提供get和delete方法处理程序。

RetrieveUpdateDestroyAPIView
用于读写 - 删除端点以表示单个模型实例。
提供get，put，patch和delete方法处理。


```python
'''urls.py'''
url(r'^booklist/$',views.Book2ListAPIView.as_view())
```


```python
'''views.py'''

class Book2ListAPIView(ListAPIView):

    # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器类
    serializer_class = BookSerializer
```


7.视图集Viewset
APIView,GenericAPIView,ListAPIView 都是继承自View
继承自View的类视图，只能定义相同的一个函数名，例如：只能定义一个get，post方法

列表视图中 设置了 queryset,serializer_class get,post
详情视图中也设置了 queryset,serializer_class get,put,delete
能否将这两个视图合并？？？
我们是可以将 列表和详情视图 组合到一起的，称之为 视图集 ViewSet
它不提供任何方法处理程序( 如get(),post() )，而是提供了诸如list() create()之类的操作


```python
class BookViewSet(ViewSet):

    # get
    def list(self,request):
        queryset = BookInfo.objects.all()
        serializer = BookInfoSerializer(queryset,many=True)
        return Response(serializer.data)
    # get
    def retrieve(self,request,pk=None):
        queryset = BookInfo.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = BookInfoSerializer(user)
        return Response(serializer.data)
```


```python
'''urls.py'''
# 继承自 ViewSet的url 可以自动生成
from rest_framework.routers import DefaultRouter,SimpleRouter

# Router:的相同点  都是可以自动生成url
# Router:的不同点
    #       DefaultRouter    可以在根路由下显示
    #       SimpleRouter     不可以在根路由下显示，且会报404
```

   

```python
# 1.创建router对象
router = DefaultRouter()

# 2.设置正则
# router的原理
# router 会自动生成两个url   一个是列表视图的url  另一个是详情视图的url

# 参数1：正则，  只需要设置列表视图和详情视图公共的部分
    # 例如：  booklist/是列表视图
            #   booklist/id 是详情视图
            # 公共部分是 booklist  不包括/
# 参数2：视图集
# 参数3：base_name  只是我们名字url name的一个前缀
        # 例如：列表视图的名字： base_name-list     book-list
        #       详情视图的名字: base_name-detail    book-detail
router.register(r'booklist',views.BookModelViewset,base_name='book')

# 3.将自动生成的url  添加到 urlpatterns中
# router.urls  urls 这个属性 存放了自动生成的url
urlpatterns +=  router.urls
```




```python
# ModelViewSet 其实就是继承自 GenericAPIView，同时继承了5个扩展
class BookModelViewset(ModelViewSet):

    queryset = BookInfo.objects.all()
    serializer_class = BookSerializer
```
