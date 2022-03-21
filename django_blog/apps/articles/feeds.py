from django.contrib.syndication.views import Feed
from apps.articles.models import Article


class AllArticleRssFeed(Feed):
    # 显示在聚会阅读器上的标题
    title = '华洛凰的博客的更新'
    # 跳转网址，为主页
    link = "/blog/index/"
    # 描述内容
    description = '关注华洛凰的最新动态'

    # 需要显示的内容条目，这个可以自己挑选一些热门或者最新的博客
    def items(self):
        return Article.objects.all()[:100]

    # 显示的内容的标题,这个才是最主要的东西
    def item_title(self, item):
        return "【{}】{}".format(item.category, item.title)

    # 显示的内容的描述
    def item_description(self, item):
        return item.body_to_markdown()