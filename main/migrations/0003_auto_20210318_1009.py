# Generated by Django 3.1.7 on 2021-03-18 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='engine',
        ),
        migrations.AddField(
            model_name='display',
            name='comments',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.comment', verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='engine',
            name='comments',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.comment', verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='user',
            name='comments',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.comment', verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='wheel',
            name='comments',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.comment', verbose_name='Комментарий'),
        ),
    ]
