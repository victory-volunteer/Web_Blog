from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class BaseModel(models.Model):
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    create_time = models.DateField(default=datetime.now, verbose_name='实体生成日期')

    class Meta:
        abstract = True


class UserProfile(AbstractUser):
    address = models.TextField(verbose_name='个人简介', default='该博主很懒，未填写任何内容')

    link = models.URLField(verbose_name='个人网址', blank=True, help_text='请填写以http开头的完整形式')
    # image = models.ImageField(verbose_name='头像', upload_to='head_image/%Y/%m', default='upimage/default.png', null=True,
    #                           blank=True)
    # 扩展用户头像字段
    image = ProcessedImageField(upload_to='avatar/%Y/%m/%d', default='avatar/default.png', verbose_name='头像',
                                processors=[ResizeToFill(80, 80)])

    # 这里使用了imagekit的ProcessedImageField，而不是django自带的ImageField。
    # 这里ProcessedImageField与ImageField类似，只不过你可以指定存储图片的大小，格式和质量。
    # 你上传的图片会先经由imagekit处理，再进行存储。缩略图thumb默认为空，因为你不需要上传，而直接由上传的image压缩生成。

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
