# Generated by Django 2.2 on 2020-11-25 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0015_auto_20201122_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(help_text='请务必填写', unique=True),
        ),
    ]