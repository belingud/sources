#### django源码分析



#### django源码分析-model概述

Django项目中提供了内置的orm框架，只需要在models.py文件中添加相关的表结构和指定的字段，就可以很方便的通过Django的orm查询从数据库中查找到相关结果，并映射到models.py中定义的类上的属性值，本文就简单概述一下，Django中的models.py中相关Models的定义与初始化过程。

本文沿用celery_django中的项目框架，在celery_app应用下的models.py文件中，暂且使用如下的内容；

```python
# Create your models here.

from django.db import models


class ThirdParty(models.Model):
    name = models.CharField(max_length=30, null=False,
                            default="首营交换", verbose_name="第三方网站名称")
    site = models.CharField(max_length=30, null=True,
                            blank=True, verbose_name="第三方域名")
    secret = models.CharField(max_length=32, null=True)
    appid = models.CharField(max_length=8, null=True)
    is_valid = models.BooleanField(default=True)
    host = models.CharField(
        max_length=50, verbose_name="app所在第三方的域名", default=None, null=True)
    ip = models.CharField(max_length=16, verbose_name="请求方服务器ip", null=False)
    redirect_url = models.CharField(
        max_length=100, verbose_name="首页重定向链接", default=None, null=True)


class ThirdUser(models.Model):
    third_party = models.ForeignKey(
        'ThirdParty', verbose_name='第三方来源', null=False)
    third_uuid = models.CharField(
        max_length=64, verbose_name='第三方用户的唯一识别码', null=False)
    email = models.EmailField(max_length=64, verbose_name='第三方用户邮箱', null=True)
    mobile = models.CharField(max_length=20, verbose_name='第三方用户手机', null=True)
    name = models.CharField(max_length=64, verbose_name='第三方用户名称', null=True)
```

其中定义了两张表结构，一个是ThirdParty表结构，一个是ThirdUser表结构，里面的字段的内容定义如上所示。

#### Model表中的初始化过程

首先需要先分析一下ThirdParty表所继承的models.Model类，该类的基本信息；

```python
class Model(six.with_metaclass(ModelBase)):

    def __init__(self, *args, **kwargs):
        signals.pre_init.send(sender=self.__class__, args=args, kwargs=kwargs)

        # Set up the storage for instance state
        self._state = ModelState()
         ...
```

该类继承自six.with_metaclass(ModelBase)处理后的类查看with_metaclass方法；

```python
def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class metaclass(meta):

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)                             // 已传入的meta生成一个name，bases为基类，d属性的类
    return type.__new__(metaclass, 'temporary_class', (), {})       // 利用type新生成一个metaclass，类名为temporary_class
```

通过该方法可知，就是调用了meta的new方法，新增了传入的类名为temporary_class，属性和父类都为空的类，此时的meta就是传入的ModelBase类；即此时的新生成的类是没有继承的父类和属性方法的，继续查看ModelBase类的信息；

```python
class ModelBase(type):
    """
    Metaclass for all models.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(ModelBase, cls).__new__
         ...
```

从继承可知ModelBase继承自type类型，并重写了**new**方法，即在加载的时候就会调用该方法进行初始化，在Django项目启动的时候，会依次加载遍历每个app，然后加载app中的model.py文件的内容，然后就会调用到每个表类的ModelBase中的**new**方法，给该类添加相关属性；

```python
class ModelBase(type):
    """
    Metaclass for all models.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(ModelBase, cls).__new__                           # 生成实例

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, ModelBase)]            # 如果继承的父类中有ModelBase类
        if not parents:
            return super_new(cls, name, bases, attrs)                       # 则直接生成该类

        # Create the class.
        module = attrs.pop('__module__')                                    # 设置module信息
        new_class = super_new(cls, name, bases, {'__module__': module})     # 生成class类
        attr_meta = attrs.pop('Meta', None)                                 # 获取属性中的Meta属性
        abstract = getattr(attr_meta, 'abstract', False)                    # 获取Meta中是否有抽象类属性值
        if not attr_meta:                                                   # 如果没有Meta
            meta = getattr(new_class, 'Meta', None)                         # 获取实例类中的Meta
        else:
            meta = attr_meta                                                # 如果已经有则设置传入的属性值
        base_meta = getattr(new_class, '_meta', None)                       # 获取新生成类的_meta属性

        app_label = None                                                    # 类标签

        # Look for an application configuration to attach the model to.
        app_config = apps.get_containing_app_config(module)                 # 获取app_config

        if getattr(meta, 'app_label', None) is None:                        # 如果获取的app_label为空
            if app_config is None:                                          # app_config为空
                if not abstract:                                            # 如果不是抽象类则报错
                    raise RuntimeError(
                        "Model class %s.%s doesn't declare an explicit "
                        "app_label and isn't in an application in "
                        "INSTALLED_APPS." % (module, name)
                    )

            else:
                app_label = app_config.label                                # 否则设置标签，即app定义的标签名

        new_class.add_to_class('_meta', Options(meta, app_label))           # 新生成的new_class上添加_meta属性
        if not abstract:                                                    # 如果不是抽象类
            new_class.add_to_class(
                'DoesNotExist',
                subclass_exception(
                    str('DoesNotExist'),
                    tuple(
                        x.DoesNotExist for x in parents if hasattr(x, '_meta') and not x._meta.abstract
                    ) or (ObjectDoesNotExist,),
                    module,
                    attached_to=new_class))                                 # 添加DoesNotExist属性
            new_class.add_to_class(
                'MultipleObjectsReturned',
                subclass_exception(
                    str('MultipleObjectsReturned'),
                    tuple(
                        x.MultipleObjectsReturned for x in parents if hasattr(x, '_meta') and not x._meta.abstract
                    ) or (MultipleObjectsReturned,),
                    module,
                    attached_to=new_class))                                 # 添加MultipleObjectsReturned属性
            if base_meta and not base_meta.abstract:                        # 如果base_meta有值，并且不是抽象类，就是多层继承的情况下
                # Non-abstract child classes inherit some attributes from their
                # non-abstract parent (unless an ABC comes before it in the
                # method resolution order).
                if not hasattr(meta, 'ordering'):
                    new_class._meta.ordering = base_meta.ordering                   # 添加ordering
                if not hasattr(meta, 'get_latest_by'):
                    new_class._meta.get_latest_by = base_meta.get_latest_by         # 添加get_latest_by属性

        is_proxy = new_class._meta.proxy                                            # 获取是否是代理属性值

        # If the model is a proxy, ensure that the base class
        # hasn't been swapped out.
        if is_proxy and base_meta and base_meta.swapped:
            raise TypeError("%s cannot proxy the swapped model '%s'." % (name, base_meta.swapped))

        # Add all attributes to the class.
        for obj_name, obj in attrs.items():                                         # 将所有的models中的属性字段都设置到新生成的class实例上
            new_class.add_to_class(obj_name, obj)

        # All the fields of any type declared on this model
        new_fields = chain(
            new_class._meta.local_fields,
            new_class._meta.local_many_to_many,
            new_class._meta.private_fields
        )                                                                           # 收集所有的fields
        field_names = {f.name for f in new_fields}                                  # 获取所有新建fields的名称

        # Basic setup for proxy models.
        if is_proxy:                                                                # 如果是代理类则建立代理相关的逻辑
            base = None
            for parent in [kls for kls in parents if hasattr(kls, '_meta')]:
                if parent._meta.abstract:
                    if parent._meta.fields:
                        raise TypeError(
                            "Abstract base class containing model fields not "
                            "permitted for proxy model '%s'." % name
                        )
                    else:
                        continue
                if base is None:
                    base = parent
                elif parent._meta.concrete_model is not base._meta.concrete_model:
                    raise TypeError("Proxy model '%s' has more than one non-abstract model base class." % name)
            if base is None:
                raise TypeError("Proxy model '%s' has no non-abstract model base class." % name)
            new_class._meta.setup_proxy(base)
            new_class._meta.concrete_model = base._meta.concrete_model
        else:
            new_class._meta.concrete_model = new_class                              # 否则设置_meta中的concrete_model为新生成的类实例

        # Collect the parent links for multi-table inheritance.
        parent_links = {}
        for base in reversed([new_class] + parents):                                # 遍历所有的类
            # Conceptually equivalent to `if base is Model`.
            if not hasattr(base, '_meta'):                                          # 如果没有_meta属性则继续遍历
                continue
            # Skip concrete parent classes.
            if base != new_class and not base._meta.abstract:                       # 如果不等于该类并且父类不是抽象类
                continue
            # Locate OneToOneField instances.
            for field in base._meta.local_fields:                                   # 遍历父类的字段
                if isinstance(field, OneToOneField):                                # 如果有字段名称为一对一字段
                    related = resolve_relation(new_class, field.remote_field.model) # 重新生成类和field的对应关系
                    parent_links[make_model_tuple(related)] = field                 # 按照新对应的app.model存入该field

        # Track fields inherited from base models.
        inherited_attributes = set()
        # Do the appropriate setup for any model parents.
        for base in new_class.mro():                                                # 获取所有继承的类
            if base not in parents or not hasattr(base, '_meta'):                   # 检查是否在parents中或者是否有_meta属性
                # Things without _meta aren't functional models, so they're
                # uninteresting parents.
                inherited_attributes |= set(base.__dict__.keys())                   # 获取所有属性后继续循环
                continue

            parent_fields = base._meta.local_fields + base._meta.local_many_to_many      # 获取所有父类的本地字段和本地多对多字段
            if not base._meta.abstract:                                                 # 如果父类不是抽象类
                # Check for clashes between locally declared fields and those
                # on the base classes.
                for field in parent_fields:                                             # 依次遍历所有父类的字段
                    if field.name in field_names:                                       # 如果父类的字段名称和该类的字段名称重复则报错
                        raise FieldError(
                            'Local field %r in class %r clashes with field of '
                            'the same name from base class %r.' % (
                                field.name,
                                name,
                                base.__name__,
                            )
                        )
                    else:
                        inherited_attributes.add(field.name)                            # 不重复就添加该父类属性名称

                # Concrete classes...
                base = base._meta.concrete_model                                        # 获取父类的实例
                base_key = make_model_tuple(base)                                       # 获取app.model key
                if base_key in parent_links:                                            # 如果该key在parents_links中
                    field = parent_links[base_key]                                      # 获取该filed
                elif not is_proxy:                                                      # 如果不在并不是代理类
                    attr_name = '%s_ptr' % base._meta.model_name                        # 获取该属性名称
                    field = OneToOneField(
                        base,
                        on_delete=CASCADE,
                        name=attr_name,
                        auto_created=True,
                        parent_link=True,
                    )                                                                   # 设置一对一filed
                    if attr_name in field_names:                                        # 检查属性名是否已经存在
                        raise FieldError(
                            "Auto-generated field '%s' in class %r for "
                            "parent_link to base class %r clashes with "
                            "declared field of the same name." % (
                                attr_name,
                                name,
                                base.__name__,
                            )
                        )

                    # Only add the ptr field if it's not already present;
                    # e.g. migrations will already have it specified
                    if not hasattr(new_class, attr_name):                               # 如果没有改属性名称则设置进去
                        new_class.add_to_class(attr_name, field)
                else:
                    field = None                                                        # 否则设置为空
                new_class._meta.parents[base] = field                                   # 设置_meta.parents设置filed
            else:
                base_parents = base._meta.parents.copy()                                # 复制parents

                # Add fields from abstract base class if it wasn't overridden.
                for field in parent_fields:                                             # 遍历父类的字段
                    if (field.name not in field_names and
                            field.name not in new_class.__dict__ and
                            field.name not in inherited_attributes):                    # 父类字段值名称不和该类字段名称有重复并且父类字段名称不和本类的其它属性值重复并且字段名称不在继承的属性值中
                        new_field = copy.deepcopy(field)                                # 深拷贝
                        new_class.add_to_class(field.name, new_field)                   # 添加该字段属性
                        # Replace parent links defined on this base by the new
                        # field. It will be appropriately resolved if required.
                        if field.one_to_one:                                            # 如果是一对一字段
                            for parent, parent_link in base_parents.items():            # 遍历父类
                                if field == parent_link:                                # 如果相等
                                    base_parents[parent] = new_field                    # 重新指向新拷贝的字段

                # Pass any non-abstract parent classes onto child.
                new_class._meta.parents.update(base_parents)                            # 将修改后的parents更新

            # Inherit private fields (like GenericForeignKey) from the parent
            # class
            for field in base._meta.private_fields:                                     # 遍历父类的私有字段
                if field.name in field_names:                                           # 如果字段名称在该类字段名称中
                    if not base._meta.abstract:                                         # 如果该父类不是抽象类则报错
                        raise FieldError(
                            'Local field %r in class %r clashes with field of '
                            'the same name from base class %r.' % (
                                field.name,
                                name,
                                base.__name__,
                            )
                        )
                else:
                    new_class.add_to_class(field.name, copy.deepcopy(field))            # 否则添加深拷贝的字段

        if abstract:                                                                # 是否是抽象类
            # Abstract base models can't be instantiated and don't appear in
            # the list of models for an app. We do the final setup for them a
            # little differently from normal models.
            attr_meta.abstract = False
            new_class.Meta = attr_meta
            return new_class                                                        # 设置类属性并返回

        new_class._prepare()                                                        # 调用类的准备方法，主要设置objects属性为manager止
        new_class._meta.apps.register_model(new_class._meta.app_label, new_class)   # 注册到app中
        return new_class                                                            # 返回类实例
```

当在加载的时候，就会执行如上，代码，主要就是检查是否是抽象类，如果继承了父类将父类的字段属性重新设置到该类上，除了处理从父类继承的属性值之外，里面主要做的工作就是设置_meta属性和model实例等工作，并且调用了new_class.add_to_class，由于该处涉及到了有关Python元类编程的相关知识，大家可自行查阅相关资料；此时主要分析一下add_to_class方法；

```python
def add_to_class(cls, name, value):
    # We should call the contribute_to_class method only if it's bound
    if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):        # 如果value是class 并且value拥有contribute_to_class属性
        value.contribute_to_class(cls, name)                                        # 调用value.contribute_to_class方法
    else:
        setattr(cls, name, value)                                                   # 否则按照正常的属性设值方法
```

此时的value就是models.py中定义的对应的属性字段值；

```python
class ThirdParty(models.Model):
    name = models.CharField(max_length=30, null=False,
                            default="首营交换", verbose_name="第三方网站名称")
```

如上所述，则value就是models.CharField该类，此时就是调用了该类的contribute_to_class方法，此时就需要查看ChareField相关的类信息；

```python
class CharField(Field):
    description = _("String (up to %(max_length)s)")

    def __init__(self, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))
        ...

@total_ordering
@python_2_unicode_compatible
class Field(RegisterLookupMixin):
    """Base class for all field types"""

    # Designates whether empty strings fundamentally are allowed at the
    # database level.
    empty_strings_allowed = True
    empty_values = list(validators.EMPTY_VALUES)

    # These track each time a Field instance is created. Used to retain order.
    # The auto_creation_counter is used for fields that Django implicitly
    # creates, creation_counter is used for all user-specified fields.
    creation_counter = 0
    auto_creation_counter = -1
    default_validators = []  # Default set of validators
    default_error_messages = {
        'invalid_choice': _('Value %(value)r is not a valid choice.'),
        'null': _('This field cannot be null.'),
        'blank': _('This field cannot be blank.'),
        'unique': _('%(model_name)s with this %(field_label)s '
                    'already exists.'),
        # Translators: The 'lookup_type' is one of 'date', 'year' or 'month'.
        # Eg: "Title must be unique for pub_date year"
        'unique_for_date': _("%(field_label)s must be unique for "
                             "%(date_field_label)s %(lookup_type)s."),
    }
    ...
```

由此可知Field就是CharField的父类，通过查看类方法可知，此时调用的就是父类Field的contribute_to_class;

```python
def contribute_to_class(self, cls, name, private_only=False, virtual_only=NOT_PROVIDED):
    """
    Register the field with the model class it belongs to.

    If private_only is True, a separate instance of this field will be
    created for every subclass of cls, even if cls is not an abstract
    model.
    """
    if virtual_only is not NOT_PROVIDED:
        warnings.warn(
            "The `virtual_only` argument of Field.contribute_to_class() "
            "has been renamed to `private_only`.",
            RemovedInDjango20Warning, stacklevel=2
        )
        private_only = virtual_only
    self.set_attributes_from_name(name)                                             # 设置字段对应的名称
    self.model = cls                                                                # 设置该字段对应的model
    if private_only:                                                                # 是否设置为私有默认不私有
        cls._meta.add_field(self, private=True)
    else:
        cls._meta.add_field(self)                                                   # 调用_meta的add_field方法
    if self.column:
        # Don't override classmethods with the descriptor. This means that
        # if you have a classmethod and a field with the same name, then
        # such fields can't be deferred (we don't have a check for this).
        if not getattr(cls, self.attname, None):
            setattr(cls, self.attname, DeferredAttribute(self.attname, cls))
    if self.choices:
        setattr(cls, 'get_%s_display' % self.name,
                curry(cls._get_FIELD_display, field=self))                          # 设置display方法
```

此时就将对应的字段值设置进去了，由于此时调用了cls._meta.add_field，_meta的属性值如下；

```python
new_class.add_to_class('_meta', Options(meta, app_label))
```

即调用了Options(meta, app_label)实例的contribute_to_class方法，此时查看Options的该方法；

```python
def contribute_to_class(self, cls, name):
    from django.db import connection
    from django.db.backends.utils import truncate_name

    cls._meta = self                                                    # 设置_meta属性值为自己
    self.model = cls                                                    # 设置model值为传入的cls
    # First, construct the default values for these options.
    self.object_name = cls.__name__                                     # 获取名称
    self.model_name = self.object_name.lower()                          # 获取model的小写名称
    self.verbose_name = camel_case_to_spaces(self.object_name)          # 获取verbose_name

    # Store the original user-defined values for each option,
    # for use when serializing the model definition
    self.original_attrs = {}                                            # 获取属性字典

    # Next, apply any overridden values from 'class Meta'.
    if self.meta:                                                       # 如果初始化传入的meta有数据
        meta_attrs = self.meta.__dict__.copy()                          # 拷贝一份meta属性
        for name in self.meta.__dict__:                                 # 遍历列表
            # Ignore any private attributes that Django doesn't care about.
            # NOTE: We can't modify a dictionary's contents while looping
            # over it, so we loop over the *original* dictionary instead.
            if name.startswith('_'):                                    # 如果已_开头的属性则删除
                del meta_attrs[name]
        for attr_name in DEFAULT_NAMES:                                 # 遍历默认的名称
            if attr_name in meta_attrs:                                 # 如果默认的名称出现在了meta的属性列表中
                setattr(self, attr_name, meta_attrs.pop(attr_name))     # 设置到自己属性中并删除meta中的属性
                self.original_attrs[attr_name] = getattr(self, attr_name)   # 保存到original_attrs字典中
            elif hasattr(self.meta, attr_name):                         # 如果meta已经有了该属性
                setattr(self, attr_name, getattr(self.meta, attr_name))     # 重新设置到自己属性中
                self.original_attrs[attr_name] = getattr(self, attr_name)   # 保存到original_attrs字典中

        self.unique_together = normalize_together(self.unique_together)     # 检查是否有unique_together字段
        self.index_together = normalize_together(self.index_together)       # 检查是否有索引字段

        # verbose_name_plural is a special case because it uses a 's'
        # by default.
        if self.verbose_name_plural is None:                                # verbose_name_plural为空则设置为's'
            self.verbose_name_plural = string_concat(self.verbose_name, 's')

        # order_with_respect_and ordering are mutually exclusive.
        self._ordering_clash = bool(self.ordering and self.order_with_respect_to)

        # Any leftover attributes must be invalid.
        if meta_attrs != {}:                                                # 如果处理完成后不为空则证明Meta中有不合法的属性值
            raise TypeError("'class Meta' got invalid attribute(s): %s" % ','.join(meta_attrs.keys()))
    else:
        self.verbose_name_plural = string_concat(self.verbose_name, 's')
    del self.meta                                                           # 删除self.meta属性

    # If the db_table wasn't provided, use the app_label + model_name.
    if not self.db_table:                                                   # 如果没有提供数据库名称则使用app.model的形式生成数据库表名
        self.db_table = "%s_%s" % (self.app_label, self.model_name)
        self.db_table = truncate_name(self.db_table, connection.ops.max_name_length())
```

主要是对Meta类中的属性值进行了检查和重新设置，最后并设置了数据库表明等操作，此时调用的cls._meta.add_filed()就是调用了该实例的该方法；

```python
def add_field(self, field, private=False, virtual=NOT_PROVIDED):
    if virtual is not NOT_PROVIDED:                                             # 是否是NOT_PROVIDED
        warnings.warn(
            "The `virtual` argument of Options.add_field() has been renamed to `private`.",
            RemovedInDjango20Warning, stacklevel=2
        )
        private = virtual
    # Insert the given field in the order in which it was created, using
    # the "creation_counter" attribute of the field.
    # Move many-to-many related fields from self.fields into
    # self.many_to_many.
    if private:                                                                 # 如果是私有字段则添加到私有列表中
        self.private_fields.append(field)
    elif field.is_relation and field.many_to_many:                              # 如果是多对多字段则添加到多对多列表中
        self.local_many_to_many.insert(bisect(self.local_many_to_many, field), field)
    else:
        self.local_fields.insert(bisect(self.local_fields, field), field)       # 插入local_fields中
        self.setup_pk(field)                                                    # 建立主键

    # If the field being added is a relation to another known field,
    # expire the cache on this field and the forward cache on the field
    # being referenced, because there will be new relationships in the
    # cache. Otherwise, expire the cache of references *to* this field.
    # The mechanism for getting at the related model is slightly odd -
    # ideally, we'd just ask for field.related_model. However, related_model
    # is a cached property, and all the models haven't been loaded yet, so
    # we need to make sure we don't cache a string reference.
    if field.is_relation and hasattr(field.remote_field, 'model') and field.remote_field.model:
        try:
            field.remote_field.model._meta._expire_cache(forward=False)
        except AttributeError:
            pass
        self._expire_cache()                                                    # 检查是否需要更新缓存
    else:
        self._expire_cache(reverse=False)
```

至此，model中的对应字段就都设置到了对应的model表的属性中了，此时orm的前部分，字段和字段类型对应的实例都已经设置完成。