from django.conf.urls import url
from apps.articles.views import IndexView, CategoryView, AboutView, ArticleView, LoveView, ArchiveView, Tag_CloudView, \
    ApplyView, SponsorView, ProcessView, AnswerView, DailyView, MySearchView,CommentView
from haystack.views import SearchView

urlpatterns = [
    url(r'^index/$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<big_slug>[A-Z_a-z0-9]*)/(?P<small_slug>[A-Z_a-z0-9]*)', CategoryView.as_view(),
        name='category'),
    url(r'^about_author/$', AboutView.as_view(), name='about'),  # 关于作者
    url(r'^article/(?P<slug>.*?)/$', ArticleView.as_view(), name='article'),
    url(r'^love/$', LoveView.as_view(), name='love'),  # 点击喜欢
    url(r'^comment/$', CommentView.as_view(), name='comment'),  # 提交评论

    url(r'^archive/(?P<dateline>[0-9-]*)/$', ArchiveView.as_view(), name='archive'),  # 文章归档
    url(r'^tag_cloud/(?P<tag_cloud>[0-9]*)/$', Tag_CloudView.as_view(), name='tag_cloud'),  # 标签云
    url(r'^friendlink_apply/$', ApplyView.as_view(), name='apply'),  # 标签云
    # url(r'^sponsor_author/$', SponsorView.as_view(), name='sponsor'),  # 赞助作者
    url(r'^answer/$', AnswerView.as_view(), name='answer'),  # 答疑解惑

    url(r'^creative_process/$', ProcessView.as_view(), name='process'),  # 创作历程
    url(r'^daily_article/$', DailyView.as_view(), name='daily'),  # 博文总览

    url(r'^search/$', MySearchView.as_view(), name='search_view'),  # 全文检索
    # url(r'search/$', SearchView(), name='search_view'),
]
