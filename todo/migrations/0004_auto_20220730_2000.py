# Generated by Django 3.2.12 on 2022-07-30 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_auto_20220730_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='level',
            field=models.SmallIntegerField(choices=[(2, '优先任务'), (1, '普通任务'), (0, '不紧急任务'), (3, '突发紧急任务')], default=0, verbose_name='任务重要性'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '进行中'), (3, '已过期'), (0, '未开始'), (2, '已完成')], default=0, verbose_name='任务状态'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='tag',
            field=models.SmallIntegerField(choices=[(6, '其他'), (0, '运动'), (2, '饮食'), (3, '工作'), (5, '生活'), (4, '休闲'), (1, '学习')], default=0, verbose_name='标签'),
        ),
    ]