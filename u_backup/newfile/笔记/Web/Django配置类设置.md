## Django使用缓存

### 使用Redis做缓存

- 常见的有两个实现

  - django-redis
    - <http://django-redis-chs.readthedocs.io/zh_CN/latest/#django>
  - django-redis-cache
    - ·<https://pypi.python.org/pypi/django-redis-cache/>

- 配置和内置的缓存配置基本一致

  - ```python
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
    ```

### Django内置的缓存

#### 缓存配置

1. 创建缓存表

   ```python
   python manage.py createcachetable [table_name]
   ```

2. 缓存配置

   ```python
   # 使用数据库中的表
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
           'LOCATION': 'my_cache_table',
           'TIMEOUT': '60',
           'OPTIONS': {
               'MAX_ENTRIES': '300',
           },
           'KEY_PREFIX': 'rock',
           'VERSION': '1',
       }
   }
   ```

- 获取cache

  - ```python
    from django.core.cache import caches
    cache = caches['cache_name']
    ```

- 获取cache

  - ```python
    from django.core.cache import cache
    cache.get("cache_name")
    ```



### DjangoRESTframework

#### 节流

在setting.py中设置全局属性

```python
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_RATES": {
        "visit_rate": "10/m",  # 1分钟10次，同理，5/s,5/h,5/d，表示秒/时/日
    }
}
```

在新建的throttle.py文件中

```python
class VisitThrottle(SimpleRateThrottle):
    scope = "visit_rate"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
```

在views视图中

```python
throttle_classes = VisitThrottle,
```

