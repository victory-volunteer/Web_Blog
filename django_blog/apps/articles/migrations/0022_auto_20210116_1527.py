# Generated by Django 2.2 on 2021-01-16 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0021_auto_20201209_2109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentuser',
            options={'ordering': ['create_date'], 'verbose_name': '评论内容', 'verbose_name_plural': '评论内容'},
        ),
        migrations.AddField(
            model_name='commentuser',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='commentuser_child_comments', to='articles.CommentUser', verbose_name='父评论'),
        ),
        migrations.AddField(
            model_name='commentuser',
            name='rep_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='commentuser_rep_comments', to='articles.CommentUser', verbose_name='回复'),
        ),
    ]