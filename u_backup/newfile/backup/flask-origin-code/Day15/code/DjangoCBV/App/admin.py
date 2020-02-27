import random

from django.contrib import admin

from App.models import Book, Student, Grade


class BookAdmin(admin.ModelAdmin):

    def is_sale(self):
        if self.b_sale:
            return "%d折" % random.randrange(10)
        else:
            return ""

    is_sale.short_description = "折扣"

    list_display = "b_name", "b_price", is_sale

    search_fields = "b_name",

    list_filter = "b_price",

    ordering = "-b_price", "-id",

    list_per_page = 30

    fieldsets = (
        ("基本信息", {"fields": ("b_name",)}),

        ("不想看的信息", {"fields": ("b_price",)}),
    )


# 注册模型的时候，制定模型的管理器
admin.site.register(Book, BookAdmin)


class StudentInfo(admin.TabularInline):
    model = Student
    extra = 3


class GradeAdmin(admin.ModelAdmin):
    inlines = StudentInfo,


admin.site.register(Grade, GradeAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = "s_name",


admin.site.register(Student,StudentAdmin)


class MyAdmin(admin.AdminSite):
    site_url = "/app/index/"
    site_title = "Rock后台"
    site_header = "Rock"


site = MyAdmin()
site.register(Book)
