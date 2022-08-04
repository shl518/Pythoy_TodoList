from django.db import models
from django.contrib.auth.models import User

level_choices = {
    (0, "不紧急任务"),
    (1, "普通任务"),
    (2, "优先任务"),
    (3, "突发紧急任务"),
}
status_choices = {
    (0, "未开始"),
    (1, "进行中"),
    (2, "已完成"),
    (3, "已过期"),
}

tag_choices = {
    (0, "运动"),
    (1, "学习"),
    (2, "饮食"),
    (3, "工作"),
    (4, "休闲"),
    (5, "生活"),
    (6, "其他"),
}


# Create your models here.
class Todo(models.Model):
    title = models.CharField(verbose_name="标题", max_length=100)
    memo = models.TextField(verbose_name="内容", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)  # 不要用这个，没有用
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.SmallIntegerField(verbose_name="任务重要性", choices=level_choices, default=0)
    expiration_date = models.DateTimeField(verbose_name="任务截止日期", null=True, blank=True)
    status = models.SmallIntegerField(verbose_name="任务状态", choices=status_choices, default=0)
    predict_hour = models.IntegerField(verbose_name="预计花费小时", default=0)
    predict_minute = models.IntegerField(verbose_name="预计花费分钟", default=0)
    isDaily = models.BooleanField(verbose_name="日常", default=False)
    fixedTime_start = models.TimeField(verbose_name="日常任务固定时间开始", null=True, blank=True)
    fixedTime_end = models.TimeField(verbose_name="日常任务固定时间结束", null=True, blank=True)
    tag = models.SmallIntegerField(verbose_name="标签", choices=tag_choices, default=0)
    overdue = models.BooleanField(default=False)
    assign_start = models.CharField(verbose_name="开始时间", max_length=10, default='00:00')
    assign_end = models.CharField(verbose_name="结束时间", max_length=10, default='00:00')

    def __str__(self):
        return self.title
