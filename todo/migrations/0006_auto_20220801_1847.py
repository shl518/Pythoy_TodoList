# Generated by Django 3.2.12 on 2022-08-01 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20220801_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='任务截止日期'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='level',
            field=models.SmallIntegerField(choices=[(3, '突发紧急任务'), (1, '普通任务'), (0, '不紧急任务'), (2, '优先任务')], default=0, verbose_name='任务重要性'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '未开始'), (2, '已完成'), (3, '已过期'), (1, '进行中')], default=0, verbose_name='任务状态'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='tag',
            field=models.SmallIntegerField(choices=[(1, '学习'), (4, '休闲'), (0, '运动'), (3, '工作'), (5, '生活'), (6, '其他'), (2, '饮食')], default=0, verbose_name='标签'),
        ),
    ]
