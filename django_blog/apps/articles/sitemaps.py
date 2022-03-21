from django.contrib.sitemaps import Sitemap
from apps.articles.models import Article


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return '/blog/article/%s/' % obj.slug
