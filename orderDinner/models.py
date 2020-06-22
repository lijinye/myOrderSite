import datetime

from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
def validate_order_time(value):
    if value < datetime.date.today():
        raise ValidationError('请选择今天及以后的日期！')


def validate_count(value):
    if value == 0:
        raise ValidationError('订餐数量必须大于0')


class OrderInfo(models.Model):
    CHOICES = (
        ('午餐', '午餐'),
        ('晚餐', '晚餐'),
    )
    order_time = models.DateField(verbose_name="订餐日期", validators=[validate_order_time])
    name = models.ForeignKey('DepartInfo', on_delete=models.CASCADE, default='', verbose_name='部门名称')
    count = models.PositiveSmallIntegerField(verbose_name='订餐数量', default=0, validators=[validate_count])
    lunchordinner = models.CharField(max_length=6, choices=CHOICES, default='午餐', verbose_name='午/晚餐')

    def __str__(self):
        return self.order_time.strftime("%Y-%m-%d") + '_' + self.name.name + '_' + self.lunchordinner + '_' + str(
            self.count) + '份'

    class Meta:
        ordering = ["-order_time"]
        verbose_name = "订餐信息"
        verbose_name_plural = "订餐信息"
        unique_together = (("order_time", "name", "lunchordinner"),)


class DepartInfo(models.Model):
    name = models.CharField(max_length=128, verbose_name='部门名称',unique=True)
    time=models.DateTimeField(verbose_name='添加时间',auto_now_add=True)

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = "部门"

    def __str__(self):
        return self.name
