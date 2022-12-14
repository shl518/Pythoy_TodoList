# Generated by Django 4.0.6 on 2022-08-05 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('memo', models.TextField(blank=True, verbose_name='内容')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datecompleted', models.DateTimeField(blank=True, null=True)),
                ('important', models.BooleanField(default=False)),
                ('level', models.SmallIntegerField(choices=[(1, '普通任务'), (0, '不紧急任务'), (3, '突发紧急任务'), (2, '优先任务')], default=0, verbose_name='任务重要性')),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='任务截止日期')),
                ('status', models.SmallIntegerField(choices=[(2, '已完成'), (0, '未开始'), (1, '进行中'), (3, '已过期')], default=0, verbose_name='任务状态')),
                ('predict_hour', models.IntegerField(default=0, verbose_name='预计花费小时')),
                ('predict_minute', models.IntegerField(default=0, verbose_name='预计花费分钟')),
                ('isDaily', models.BooleanField(default=False, verbose_name='日常')),
                ('fixedTime_start', models.TimeField(blank=True, null=True, verbose_name='日常任务固定时间开始')),
                ('fixedTime_end', models.TimeField(blank=True, null=True, verbose_name='日常任务固定时间结束')),
                ('tag', models.SmallIntegerField(choices=[(0, '运动'), (3, '工作'), (4, '休闲'), (6, '其他'), (5, '生活'), (2, '饮食'), (1, '学习')], default=0, verbose_name='标签')),
                ('overdue', models.BooleanField(default=False)),
                ('assign_start', models.CharField(default='00:00', max_length=10, verbose_name='开始时间')),
                ('assign_end', models.CharField(default='00:00', max_length=10, verbose_name='结束时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
