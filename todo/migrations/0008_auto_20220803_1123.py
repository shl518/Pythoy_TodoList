# Generated by Django 3.2.12 on 2022-08-03 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0007_auto_20220801_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='level',
            field=models.SmallIntegerField(choices=[(0, '不紧急任务'), (1, '普通任务'), (2, '优先任务'), (3, '突发紧急任务')], default=0, verbose_name='任务重要性'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.SmallIntegerField(choices=[(2, '已完成'), (0, '未开始'), (1, '进行中'), (3, '已过期')], default=0, verbose_name='任务状态'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='tag',
            field=models.SmallIntegerField(choices=[(3, '工作'), (6, '其他'), (4, '休闲'), (0, '运动'), (1, '学习'), (2, '饮食'), (5, '生活')], default=0, verbose_name='标签'),
        ),
    ]
