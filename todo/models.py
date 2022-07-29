from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    everyday = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level_choices = {
        (0, "不紧急任务"),
        (1, "普通任务"),
        (2, "优先任务"),
        (3, "突发紧急任务"),
    }
    level = models.SmallIntegerField(verbose_name="任务重要性", choices=level_choices, default=0)
    status_choices = {
        (0, "未开始"),
        (1, "进行中"),
        (2, "已结束"),
        (3, "已过期"),
    }
    status = models.SmallIntegerField(verbose_name="任务状态", choices=status_choices, default=0)
    expiration_date = models.DateTimeField(verbose_name="任务截止日期")

    def __str__(self):
        return self.title
