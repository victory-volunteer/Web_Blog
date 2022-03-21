# Generated by Django 2.2 on 2020-11-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_auto_20201111_2134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-create_time'], 'verbose_name': '博客内容', 'verbose_name_plural': '博客内容'},
        ),
        migrations.AddField(
            model_name='rotation',
            name='is_hot',
            field=models.BooleanField(default=False, verbose_name='是否为热门专题图片'),
        ),
    ]