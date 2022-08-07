# Generated by Django 3.2.12 on 2022-08-07 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='level',
            field=models.SmallIntegerField(choices=[(0, '不紧急任务'), (2, '优先任务'), (3, '突发紧急任务'), (1, '普通任务')], default=0, verbose_name='任务重要性'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '未开始'), (1, '进行中'), (3, '已过期'), (2, '已完成')], default=0, verbose_name='任务状态'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='tag',
            field=models.SmallIntegerField(choices=[(5, '生活'), (4, '休闲'), (3, '工作'), (1, '学习'), (0, '运动'), (6, '其他'), (2, '饮食')], default=0, verbose_name='标签'),
        ),
    ]
