from django.shortcuts import render
from django.views import View
import re
from django.db.models import Q
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from pure_pagination import Paginator, PageNotAnInteger
from apps.articles.models import Article, Notice, Rotation, FriendLink, BigCategory, Category, Tag, Keyword, \
    Daily_Article, CommentUser
import time
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from haystack.generic_views import SearchView  # 导入搜索视图
from haystack.query import SearchQuerySet
from django.conf import settings
from apps.articles.forms import CommentForm
from django.urls import reverse


class IndexView(View):
    """首页内容"""

    def get(self, request, *args, **kwargs):
        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        friendlink = FriendLink.objects.filter(Q(is_active=True), Q(is_show=True))
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        rotation = Rotation.objects.all()
        tag = Tag.objects.all()
        hot_article = Article.objects.all().order_by('-views')[:5]
        love_article = Article.objects.all().order_by('-loves')[:5]
        all_article = Article.objects.all()
        article_dates = set()
        for articles in all_article:
            x = re.match(r"\d*.\d*", str(articles.create_time)).group()
            article_dates.add(x)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_article, per_page=3, request=request)
        article = p.page(page)
        return render(request, 'index.html', {'bigCategory': bigcategory, 'category': category,
                                              'rotation': rotation, 'hot_article': hot_article, 'all_article': article,
                                              'article_dates': article_dates, 'love_article': love_article,
                                              'friendlink': friendlink, 'tag': tag, 'notice': notice,

                                              })


class CategoryView(View):
    """其他页博文"""

    def get(self, request, big_slug, small_slug, *args, **kwargs):
        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        friendlink = FriendLink.objects.filter(Q(is_active=True), Q(is_show=True))
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        rotation = Rotation.objects.all()
        tag = Tag.objects.all()
        love_article = Article.objects.all().order_by('-loves')[:6]
        all_article = Article.objects.all()
        article_dates = set()
        for articles in all_article:
            x = re.match(r"\d*.\d*", str(articles.create_time)).group()
            article_dates.add(x)
        try:
            big_slug_id = BigCategory.objects.get(slug=big_slug).id
        except:
            big_slug_id = ''
        try:
            small_slug_id = Category.objects.get(slug=small_slug).id
        except:
            small_slug_id = ''
        if small_slug:
            all_article = Article.objects.filter(category_id=small_slug_id)
        elif big_slug_id:
            all_article = Article.objects.filter(bigcategory_id=big_slug_id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_article, per_page=5, request=request)
        article = p.page(page)
        return render(request, 'content.html', {'bigCategory': bigcategory, 'category': category,
                                                'rotation': rotation,
                                                'all_article': article,
                                                'article_dates': article_dates, 'love_article': love_article,
                                                'friendlink': friendlink, 'tag': tag, 'notice': notice,
                                                'big_slug': big_slug, 'small_slug': small_slug
                                                })


class AboutView(View):
    """关于作者"""

    def get(self, request, *args, **kwargs):
        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        big_slug = 'about_author'
        return render(request, 'about.html', {'bigCategory': bigcategory, 'category': category,
                                              'notice': notice, 'big_slug': big_slug
                                              })


class ArticleView(View):
    """博文详情页"""

    def get(self, request, slug, *args, **kwargs):

        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        friendlink = FriendLink.objects.filter(Q(is_active=True), Q(is_show=True))
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        rotation = Rotation.objects.all()
        tag = Tag.objects.all()
        love_article = Article.objects.all().order_by('-loves')[:6]
        all_article = Article.objects.all()
        article_dates = set()
        for articles in all_article:
            x = re.match(r"\d*.\d*", str(articles.create_time)).group()
            article_dates.add(x)
        article = Article.objects.filter(slug=slug)
        x_article = Article.objects.get(slug=slug)
        comment_id = x_article.id
        comment = CommentUser.objects.filter(belong_id=comment_id)
        big_category = BigCategory.objects.get(id=x_article.bigcategory_id)
        small_category = Category.objects.get(id=x_article.category_id)
        big_slug = big_category.slug
        small_slug = small_category.slug
        article_tag = x_article.tags.all()
        get_article_previous = x_article.get_article_previous(x_article.id)
        get_article_next = x_article.get_article_next(x_article.id)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        article_body = md.convert(x_article.body)
        # 浏览量增加
        ses = self.request.session
        the_key = 'is_read_{}'.format(x_article.id)
        # print('1', the_key)
        is_read_time = ses.get(the_key)
        # print('2', is_read_time)
        # if self.request.user != x_article.author: # 待处理
        if not is_read_time:
            x_article.update_views()
            ses[the_key] = time.time()
            # print('3', ses[the_key])
        else:
            now_time = time.time()
            # print('4', now_time)
            t = now_time - is_read_time
            # print('5', t)
            if t > 60 * 30:
                x_article.update_views()
                ses[the_key] = time.time()
                # print('6', [the_key])

        # md.toc用来在页面侧边栏显示目录(目录已经保存在模板变量toc中),只需在模板中引用这个变量即可
        return render(request, 'article.html', {'bigCategory': bigcategory, 'category': category,
                                                'rotation': rotation, 'big_slug': big_slug,
                                                'article': article, 'x_article': x_article, 'small_slug': small_slug,
                                                'article_dates': article_dates, 'love_article': love_article,
                                                'friendlink': friendlink, 'tag': tag, 'notice': notice,
                                                'big_category': big_category, 'small_category': small_category,
                                                'article_tag': article_tag, 'toc': md.toc,
                                                'get_article_previous': get_article_previous,
                                                'get_article_next': get_article_next, 'article_body': article_body,
                                                'comment': comment
                                                })


class LoveView(View):
    """博文喜欢"""

    def post(self, request, *args, **kwargs):
        data_id = request.POST.get('article_id')
        if data_id:
            article = Article.objects.get(id=data_id)
            article.loves += 1
            article.save()
            return HttpResponse(article.loves)
        else:
            return HttpResponse('error', status=405)


class CommentView(View):
    """提交评论"""

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        article_id = request.POST.get('article_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        comment = CommentUser()
        comment.content = content
        comment.belong_id = article_id
        comment.nickname = username
        comment.email = email
        comment.save()
        return JsonResponse({'msg': '提交成功', })


class ArchiveView(View):
    """文章归档"""

    def get(self, request, dateline, *args, **kwargs):
        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        friendlink = FriendLink.objects.filter(Q(is_active=True), Q(is_show=True))
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        rotation = Rotation.objects.all()
        tag = Tag.objects.all()
        love_article = Article.objects.all().order_by('-loves')[:6]
        all_article = Article.objects.all()
        article_dates = set()
        article_archive = []
        for articles in all_article:
            x = re.match(r"\d*.\d*", str(articles.create_time)).group()
            article_dates.add(x)
            if x != dateline:
                article_archive.append(articles.id)
        # 归档后文章
        all_article = Article.objects.all().exclude(id__in=article_archive)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_article, per_page=5, request=request)
        article = p.page(page)
        return render(request, 'content.html', {'bigCategory': bigcategory, 'category': category,
                                                'rotation': rotation,
                                                'all_article': article,
                                                'article_dates': article_dates, 'love_article': love_article,
                                                'friendlink': friendlink, 'tag': tag, 'notice': notice,

                                                })


class Tag_CloudView(View):
    """标签云"""

    def get(self, request, tag_cloud, *args, **kwargs):
        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        friendlink = FriendLink.objects.filter(Q(is_active=True), Q(is_show=True))
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        rotation = Rotation.objects.all()
        tag = Tag.objects.all()
        love_article = Article.objects.all().order_by('-loves')[:6]
        all_article = Article.objects.all()
        article_dates = set()
        for articles in all_article:
            x = re.match(r"\d*.\d*", str(articles.create_time)).group()
            article_dates.add(x)
        # 标签云
        all_article = Tag.objects.filter(id=tag_cloud)[0].article_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_article, per_page=5, request=request)
        article = p.page(page)
        return render(request, 'content.html', {'bigCategory': bigcategory, 'category': category,
                                                'rotation': rotation,
                                                'all_article': article,
                                                'article_dates': article_dates, 'love_article': love_article,
                                                'friendlink': friendlink, 'tag': tag, 'notice': notice,
                                                })


class ApplyView(View):
    """友链申请"""

    def get(self, request, *args, **kwargs):
        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        big_slug = 'about_author'
        return render(request, 'friendlink_apply.html', {'bigCategory': bigcategory, 'category': category,
                                                         'notice': notice, 'big_slug': big_slug
                                                         })


class SponsorView(View):
    """赞助作者"""

    def get(self, request, *args, **kwargs):
        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        big_slug = 'sponsor_author'
        return render(request, 'sponsor.html', {'bigCategory': bigcategory, 'category': category,
                                                'notice': notice, 'big_slug': big_slug
                                                })


class AnswerView(View):
    """答疑解惑"""

    def get(self, request, *args, **kwargs):
        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        big_slug = 'answer'
        return render(request, 'answer.html', {'bigCategory': bigcategory, 'category': category,
                                               'notice': notice, 'big_slug': big_slug
                                               })


class ProcessView(View):
    """创作历程"""

    def get(self, request, *args, **kwargs):
        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        friendlink = FriendLink.objects.filter(Q(is_active=True), Q(is_show=True))
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        rotation = Rotation.objects.all()
        tag = Tag.objects.all()
        hot_article = Article.objects.all().order_by('-views')[:5]
        love_article = Article.objects.all().order_by('-loves')[:5]
        all_article = Article.objects.all()
        article_dates = set()
        for articles in all_article:
            x = re.match(r"\d*.\d*", str(articles.create_time)).group()
            article_dates.add(x)
        big_slug = 'creative_process'
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_article, per_page=5, request=request)
        all_article = p.page(page)
        return render(request, 'blog_overview.html', {'bigCategory': bigcategory, 'category': category,
                                                      'notice': notice, 'big_slug': big_slug,
                                                      'rotation': rotation, 'hot_article': hot_article,
                                                      'article_dates': article_dates, 'love_article': love_article,
                                                      'friendlink': friendlink, 'tag': tag, 'all_article': all_article,
                                                      })


class DailyView(View):
    """每日必读"""

    def get(self, request, *args, **kwargs):
        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        friendlink = FriendLink.objects.filter(Q(is_active=True), Q(is_show=True))
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        rotation = Rotation.objects.all()
        tag = Tag.objects.all()
        hot_article = Article.objects.all().order_by('-views')[:5]
        love_article = Article.objects.all().order_by('-loves')[:5]
        all_article = Article.objects.all()
        article_dates = set()
        for articles in all_article:
            x = re.match(r"\d*.\d*", str(articles.create_time)).group()
            article_dates.add(x)
        big_slug = 'daily_article'
        daily_article = Daily_Article.objects.all()[:10]
        return render(request, 'daily_article.html', {'bigCategory': bigcategory, 'category': category,
                                                      'notice': notice, 'big_slug': big_slug,
                                                      'rotation': rotation, 'hot_article': hot_article,
                                                      'article_dates': article_dates, 'love_article': love_article,
                                                      'friendlink': friendlink, 'tag': tag, 'all_article': all_article,
                                                      'daily_article': daily_article,
                                                      })


# 重写搜索视图，可以增加一些额外的参数，且可以重新定义名称
class MySearchView(SearchView):
    # 返回搜索结果集
    context_object_name = 'search_list'
    # 搜索结果以浏览量排序
    queryset = SearchQuerySet().order_by('-views')

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        notice = Notice.objects.filter(is_active=True).order_by('-update_date')[0]
        friendlink = FriendLink.objects.filter(Q(is_active=True), Q(is_show=True))
        bigcategory = BigCategory.objects.all()
        category = Category.objects.all()
        rotation = Rotation.objects.all()
        tag = Tag.objects.all()
        hot_article = Article.objects.all().order_by('-views')[:5]
        love_article = Article.objects.all().order_by('-loves')[:5]
        all_article = Article.objects.all()
        article_dates = set()
        for articles in all_article:
            x = re.match(r"\d*.\d*", str(articles.create_time)).group()
            article_dates.add(x)
        context['bigCategory'] = bigcategory
        context['category'] = category
        context['notice'] = notice
        context['context'] = context
        context['rotation'] = rotation
        context['hot_article'] = hot_article
        context['article_dates'] = article_dates
        context['love_article'] = love_article
        context['friendlink'] = friendlink
        context['tag'] = tag
        context['all_article'] = all_article
        return context



