# Django admin高级用法

使用Django意味着后台框架的几乎所有内容都会和Django产生互动,排除功能全部手撸的情况.

Django 后台admin有大量的属性和方法,拥有强大的功能和自定义能力.通过完整的代码来看Django admin的基础设置和高级用法,并结合form表单来实现深度自定义.



# 简单使用



如果只是使用admin自带的数据管理功能,只需要将模型注册到admin中,就可以实现.



```python
from django.contrib import admin

admin.site.register(News)
admin.site.register(NewsType)
admin.site.site_header = "数据库"
admin.site.index_title = "新闻后台"
```

Django后台会将对应数据表的所有字段进行展示,默认点击`id`会进入修改页面,对应`change_form.html`模板.


## 自定义admin类

使用admin也可以自定义一个admin的类,来自定义后台实现的属性和方法,然后通过`register()`来将自定义的类和模型注册在一起.


注册方式有两种,一种是使用类装饰器,一种是使用`site`

```python
from django.contrib import admin

# 装饰器注册
@admin.register(ModelClass)
class CustomAdmin(admin.ModelAdmin):
    list_display = '__all__'
```


```python
# 使用site
class CustomAdmin(admin.ModelAdmin):
    exclude = ['id']

admin.site.register(CustomAdmin, ModelClass)
```

# admin显示属性的设置

## ModelAdmin中的属性设置

admin可以设置在列表页和详情页显示的字段以及搜索字段等的限制,在admin的类中可以直接定义.



以使用较多的`ModelAdmin`为例,`ModelAdmin`源码中的属性有:



```python
# 在列表页显示的字段,默认会显示所有字段,有对应的方法可以重写
list_display = ('__str__',)
# 在列表页显示的字段中,可以链接到change_form页面的字段
list_display_links = ()
# 右侧的筛选,必须是字段,可以继承自SimpleListFilter来自定义筛选字段和规则,SimpleListFilter的方法在后面详细介绍
list_filter = ()
# 联表查询是否自动查询,可以是布尔,列表或元组,如果是列表或元组,则级联查询指定的字段
list_select_related = False
# 列表页每页展示的条数
list_per_page = 100
# 分页,显示全部,真是数据小于该值时才会显示全部
list_max_show_all = 200
# 在列表页可以编辑的字段
list_editable = ()
# 在列表页可以模糊搜索的字段
search_fields = ()
# 对Date和DateTime类型进行搜索
date_hierarchy = None
# 在change_form页面,按钮为,save按钮的值(save as new和save add another)
save_as = False
# 点击保存并继续编辑
save_as_continue = True
# save按钮的位置,是True则显示在页面上方
save_on_top = False
# 自定义分页类
paginator = Paginator
# 详细页面，删除、修改，更新后跳转回列表后，是否保留原搜索条件管理员现在在创建，编辑或删除对象后保留列表视图中的过滤器。
# 可以将此属性设置为False，以恢复之前清除过滤器的行为。
preserve_filters = True
# 在详情页面,如果有FK到其他表,在详情页中可以动态的填加或删除级联数据
inlines = []
```

## admin中action操作的设置

admin中的action是指在列表页的动作,默认为删除所选的条目,可以自定义填加动作,将动作注册到action中,需要是一个方法

```python
# 定制action中的操作
actions = []

action_form = helpers.ActionForm
# action选项显示的位置,页面上方或者页面下方
actions_on_top = True
actions_on_bottom = False
# 是否显示action选择的个数
actions_selection_counter = True
checks_class = ModelAdminChecks
```

## BaseModelAdmin中的属性

除了ModelAdmin中的属性,也可以自定义在其父类BaseModelAdmin中的属性和方法,是一些通用的,在继承子BaseModelAdmin的类中也可以完成的属性设置.一般是详情页的属性.

```python
# 自动补全,外键查询数据多时,方便查找
autocomplete_fields = ()
# 详情页,针对外键和M2M字段变成input框形式
raw_id_fields = ()
# 详情页面展示的字段
fields = None
# 详情页面排除的字段,字段可以是数据库中的也可以是自定义的
exclude = None
# 在详情页面对数据进行分隔显示,对应到admin模板中的'fieldsets.html'
fieldsets = None
# 为详情页指定form表单,可以自定义显示的数据,字段
form = forms.ModelForm
# 下面两个是M2M显示时,数据移动选择.可以参考admin中用户的权限操作
filter_vertical = ()  # 纵向展示
filter_horizontal = ()  # 横向展示
# 详情页面使用radio显示选项,FK默认使用select
radio_fields = {}
# 填加页面,在某字段输入值后,自动填加到指定字段
# prepopulated_fields = {"email": ("user",)},email字段会在用户填加user字段时自动填充
prepopulated_fields = {}
# 详情页指定显示的插件,后面详细说明
formfield_overrides = {}
# 详情页面的只读字段
readonly_fields = ()
# 详情页面排序规则
ordering = None
# 禁止某些排序,为空则禁止所有的排序
sortable_by = None
# 编辑时是否在页面上显示view on set,可以通过方法来返回一个链接,后面说明
view_on_site = True
# 列表页,模糊搜索后面显示的数据个数样式
# 为True是显示条数,为False时显示全部
show_full_result_count = True
checks_class = BaseModelAdminChecks
```

# 模板的定制

## 指定自定义模板

在ModelAdmin中自带了几个指定模板的属性，可以自己定义HTML文件，来指定给某个模板页面

```python
# Custom templates (designed to be over-ridden in subclasses)
# 添加数据模板页
add_form_template = None
# 修改数据的模板页
change_form_template = None
# 修改多条数据的模板页
change_list_template = None
# 删除确认信息模板页
delete_confirmation_template = None
# 删除关联数据的确认页
delete_selected_confirmation_template = None
# 修改历史的模板页
object_history_template = None
# 弹出框模板页
popup_response_template = None
```

## 重写自带模板

在django admin里面有自己写好的模板，include模板，每个app也有对应的模板


admin的自带模板在项目的`django/contrib/admin/templates/admin`，目录下面


`include`文目录下是`include`语法包含的模板。


`change_form.html`是数据修改页面的模板，如果想在数据详情页面自定义显示的内容，可以自定义这个页面


模板使用的全都是模板语法，注意模板语法的继承机制，在当前页面重写的元素，不会直接显示。


`fieldset.htlm`是拼接成详情页的块。前面提到，自定义admin类中的`fieldset`属性，可以自定义详情页，使数据字段分块显示，就是改变了传给这个页面的值。

例如，使用`if`语句来动态添加jQuery和`div`标签，只有在访问某个app的数据时添加

```html
{% if app_name in request.path %}
    <script src="http://ajax.aspnetcdn.com/ajax/jquery/jquery-2.1.4.min.js"></script>
<div>
<fieldset class="custom">

<div id="div"></div>
</fieldset>
{% endif %}
```

## 结合form表单

django admin结合form表单，重写`fieldset.html`来实现数据详情页面的深度自定义，通过处理form表单提交的数据，来实现后台功能的完全自定义。


django的admin中可以指定form类，来自定义显示的内容

```python
from django import forms
# TagValueManager是自定义的类
from tag_manager import TagValueManager

class CustomAddForm(forms.ModelForm):

    """ 根据标签的id,动态生成下拉选项框 """
    for i in TagValueManager.all_tag:
        locals()[
            'field_tag_id_{}'.format(
                i['id'])] = forms.ChoiceField(
            choices=TagValueManager.get_choice(
                i['id']),
            label=i['name'])

    class Meta:
        model = CandidateTag
        fields = '__all__'
        exclude = ['tag_id', 'tag_value', 'ext_1', 'ext_2', 'candidate_id']
```


> 注意：在form表单中动态生成的属性，必须使用`fields=’__all__‘`属性，否则不会显示，可以结合`exclude`属性来控制需要显示的表单


然后在admin中注册form类


```python
class CandidateTagAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'tag_count',
    ]
    form = CustomAddForm
```


## 自定义列表页来源

除了可以通过修改admin的属性，来实现列表页展示字段的自定义，也可以对列表页数据进行筛选，例如，筛选出活跃的用户等，这个可以在`action`中定义新的方法


也可以重写admin中的`get_queryset`方法，返回的qs是重新筛选之后的数据，可以避免一些业务逻辑上的误操作


这里的代码展示了，在列表页，展示其他表中的数据，注册模型表的数据没有展示


```python
    def get_queryset(self, request):
        """
        从candidate表中查询数据,在list_display中统计其标签个数
        """
        qs = Candidate.objects.all().order_by('id')
        return qs
```

##　处理form数据

给admin类定义form属性之后，在详情页面传回的数据，会带上form表单里面的数据，然后结合业务逻辑处理这个数据


例如，业务场景，接受form数据，保存到其他几张表，对于展示数据的表，不进行任何操作，那就需要重写`save_model`方法，这个方法调用了模型的`save`方法


重写这个方法：


```python
    def save_model(self, request, obj, form, change):
        """
        重写save_model方法
        """
        candidate_id = request.path.split('/')[4]
        post_dict = request.POST
        # 根据返回的form表单的标签来确定修改的tag_id
        include_field = 'field_tag_id_'
        for key, value in post_dict.items():
            if include_field in key:
                tag_id = key.split('_')[-1]
                tag_value = value
                try:
                    obj, created = CandidateTag.objects.update_or_create(
                        defaults={'tag_value': tag_value}, candidate_id=candidate_id, tag_id=tag_id)
                except Exception as e:
                    tag_name = TagValueManager.all_tag.get(id=tag_id)['name']
                    messages.add_message(request, messages.ERROR, '求职者的"{}"标签信息保存失败'.format(tag_name))
```

# 扩展


在`get_queryset`方法中，展示类模型中的统计数据，这个统计数据，不是在数据库中生成的，实在模型类中定义的方法，这个方法的返回值，可以在列表页中直接展示。例如上文中说道的标签的个数


同时，也可以返回一个HTML标签，模板语法中获取这个字段时，得到的是一个HTML标签，直接渲染


```python
from django.utils.safestring import mark_safe
# 使用mark_safe
@mark_safe
def get_user_dept(self,obj):
    """ 这个方法在模型中 """
    return "<p>this is a HTML tag</p>"
# 允许HTML标签
get_report_depts.allow_tags = True
# HTML展示时的字段名
get_report_depts.short_description = '所属部门'
```
