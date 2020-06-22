from datetime import date
import datetime
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Register your models here.
from . import models


@admin.register(models.OrderInfo)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_time', 'name', 'lunchordinner', 'count']
    # list_editable = ['count']
    view_on_site = False
    date_hierarchy = 'order_time'

    # list_per_page=2
    # def order_depart(self, obj):
    #     return [depart.name for depart in obj.depart_info.all()]

    # order_depart.short_description = '部门'
    # filter_horizontal = ('depart_info',)
    class DecadeBornListFilter(admin.SimpleListFilter):
        # 提供一个可读的标题
        title = _('订餐日期')

        # 用于URL查询的参数.
        parameter_name = 'order_time'

        def lookups(self, request, model_admin):
            """
            返回一个二维元组。每个元组的第一个元素是用于URL查询的真实值，
            这个值会被self.value()方法获取，并作为queryset方法的选择条件。
            第二个元素则是可读的显示在admin页面右边侧栏的过滤选项。
            """
            if datetime.date.today().isoweekday() == 1:
                yesterday = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
            else:
                yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            if datetime.date.today().isoweekday() in (6, 7):
                today = ''
            else:
                today = (datetime.datetime.now()).strftime("%Y-%m-%d")
            if datetime.date.today().isoweekday() == 5:
                tomorrow = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
            else:
                tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            if today:

                return (
                    (yesterday, _(yesterday)),
                    (today, _(today)),
                    (tomorrow, _(tomorrow)),
                )
            else:
                return (
                    (yesterday, _(yesterday)),
                    (tomorrow, _(tomorrow)),
                )

        def queryset(self, request, queryset):
            """
            根据self.value()方法获取的条件值的不同执行具体的查询操作。
            并返回相应的结果。
            """
            # if self.value() == '80s':
            #     return queryset.filter(birthday__gte=date(1980, 1, 1),
            #                            birthday__lte=date(1989, 12, 31))
            if self.value() != None:
                return queryset.filter(order_time__exact=self.value())

    # list_filter = [DecadeBornListFilter]
    list_filter = [ 'lunchordinner','name']

    # def changelist_view(self, request, extra_context=None):
    #     if request.META.get('HTTP_REFERER'):
    #         if request.META['HTTP_REFERER'].find('orderinfo') < 0:
    #             q = request.GET.copy()
    #             if datetime.date.today().isoweekday() == 5:
    #                 q['order_time'] = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    #             else:
    #                 q['order_time'] = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    #             request.GET = q
    #             request.META['QUERY_STRING'] = request.GET.urlencode()
    #     elif not request.META['QUERY_STRING']:
    #         q = request.GET.copy()
    #         if datetime.date.today().isoweekday() == 5:
    #             q['order_time'] = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    #         else:
    #             q['order_time'] = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    #         request.GET = q
    #         request.META['QUERY_STRING'] = request.GET.urlencode()
    #     return super(orderadmin, self).changelist_view(request, extra_context=extra_context)


@admin.register(models.DepartInfo)
class DepartAdmin(admin.ModelAdmin):
    list_display = ['name','time']


admin.site.site_header = '订餐系统'
admin.site.site_title = '订餐系统'
