from django.db import models
from apps.users.models import BaseModel, UserProfile
import markdown
from django.urls import reverse
import emoji


class Notice(BaseModel):
    text = models.TextField(verbose_name='公告', default='暂无公告')
    is_active = models.BooleanField(verbose_name='是否开启标志', default=False)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.text[:5]


class Rotation(BaseModel):
    number = models.IntegerField(verbose_name='播放顺序编号', blank=True, null=True)
    title = models.CharField(verbose_name='标题', max_length=20, blank=True, null=True, default='仅供欣赏')
    content = models.CharField(verbose_name='图片描述', max_length=80, blank=True, null=True)
    img_link = models.ImageField(verbose_name='图片地址', upload_to='rotation_img/%Y/%m', default='upimage/default1.png',
                                 null=True,
                                 blank=True)
    url = models.CharField(verbose_name='跳转链接', max_length=200, default='#')
    is_hot = models.BooleanField(verbose_name="是否为热门专题图片", default=False)

    class Meta:
        verbose_name = '图片轮播'
        verbose_name_plural = verbose_name
        ordering = ['number', '-id']

    def __str__(self):
        return self.title


class FriendLink(BaseModel):
    name = models.CharField(verbose_name='网站名称', max_length=50)
    description = models.CharField(verbose_name='网站描述', max_length=100, blank=True)
    link = models.URLField(verbose_name='友链地址')
    logo = models.ImageField(verbose_name='图片地址', upload_to='logo/%Y/%m', default='upimage/default1.png',
                             null=True,
                             blank=True)
    is_active = models.BooleanField(verbose_name='是否有效', default=True)
    is_show = models.BooleanField(verbose_name='是否展示', default=False)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.name


class Keyword(BaseModel):
    name = models.CharField('文章关键词', max_length=20)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(verbose_name='文章标签', max_length=20)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def article_list(self):
        return ','.join([i.title for i in self.article_set.all()])


class BigCategory(BaseModel):
    name = models.CharField(verbose_name='导航栏分类', max_length=20)
    is_show = models.BooleanField(default=False, verbose_name='是否有二级标签')
    slug = models.SlugField(unique=True, null=True, blank=True)  # 用作文章的访问路径，每篇文章有独一无二的标识

    class Meta:
        verbose_name = '导航栏分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(verbose_name='文章分类', max_length=20)
    bigcategory = models.ForeignKey(BigCategory, on_delete=models.CASCADE, verbose_name='导航栏分类')
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(BaseModel):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='作者')
    title = models.CharField(verbose_name='文章标题', max_length=200)
    body = models.TextField(verbose_name='文章内容')
    summary = models.TextField(verbose_name='文章摘要', default='作者懒的写摘要')
    img_link = models.ImageField(verbose_name='图片地址', upload_to='article_img/%Y/%m', default='upimage/default1.png',
                                 null=True,
                                 blank=True)
    views = models.IntegerField(verbose_name='浏览量', default=0)
    loves = models.IntegerField(verbose_name='喜爱量', default=0)
    comments = models.IntegerField(verbose_name='评论数', default=0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='文章二级分类', blank=True, null=True)
    bigcategory = models.ForeignKey(BigCategory, on_delete=models.DO_NOTHING, verbose_name='文章大分类', blank=True,
                                    null=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    slug = models.SlugField(unique=True, null=True, blank=False, help_text='请务必填写')
    keywords = models.ManyToManyField(Keyword, verbose_name='文章关键词',
                                      help_text='针对网站优化，那么一个网站最基本的SEO就是设置TDK，则需要一个页面关键字表 Keyword')

    class Meta:
        verbose_name = '博客内容'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.title

    def tag_list(self):
        return ','.join([i.name for i in self.tags.all()])

    # rss订阅
    def get_absolute_url(self):
        return reverse('blog:article', args=[self.slug])

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    # 获取前一篇文章，参数当前文章 ID
    def get_article_previous(self, article_id):
        has_previous = False
        id_previous = article_id
        while not has_previous and id_previous >= 1:
            article_previous = Article.objects.filter(id=id_previous - 1).first()
            if not article_previous:
                id_previous -= 1
            else:
                has_previous = True
        if has_previous:
            article = Article.objects.filter(id=id_previous - 1).first()
            return article
        else:
            return

    # 获取下一篇文章，参数当前文章 ID
    def get_article_next(self, article_id):
        has_next = False
        id_next = article_id
        article_id_max = Article.objects.all().order_by('-id').first()
        id_max = article_id_max.id
        while not has_next and id_next <= id_max:
            article_next = Article.objects.filter(id=id_next + 1).first()
            if not article_next:
                id_next += 1
            else:
                has_next = True
        if has_next:
            article = Article.objects.filter(id=id_next + 1).first()
            return article
        else:
            return

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class CommentUser(BaseModel):
    nickname = models.CharField(max_length=20, verbose_name='昵称', default='匿名用户')
    email = models.EmailField(verbose_name='邮箱', max_length=50)
    content = models.TextField(verbose_name='评论内容')
    belong = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name='所属文章')
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, verbose_name='父评论',
                               related_name='%(class)s_child_comments', blank=True,
                               null=True)
    rep_to = models.ForeignKey('self', on_delete=models.DO_NOTHING, verbose_name='回复',
                               related_name='%(class)s_rep_comments', blank=True, null=True)

    class Meta:
        verbose_name = '评论内容'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.content[:20]

    def content_to_markdown(self):
        # 先转换成emoji然后转换成markdown,'escape':所有原始HTML将被转义并包含在文档中
        to_emoji_content = emoji.emojize(self.content, use_aliases=True)
        to_md = markdown.markdown(to_emoji_content,
                                  safe_mode='escape',
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                  ])
        return to_md


class Daily_Article(BaseModel):
    title = models.CharField(verbose_name='文章标题', max_length=200)
    body = models.TextField(verbose_name='文章内容')
    summary = models.TextField(verbose_name='文章摘要', default='作者懒的写摘要')
    img_link = models.ImageField(verbose_name='图片地址', upload_to='daily_article_img/%Y/%m',
                                 default='upimage/default1.png',
                                 null=True,
                                 blank=True)
    slug = models.SlugField(unique=True, null=True, blank=False, help_text='请务必填写')

    class Meta:
        verbose_name = '每日必读'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
