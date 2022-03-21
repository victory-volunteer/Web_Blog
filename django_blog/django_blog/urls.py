from django.urls import path
import xadmin
from django.conf.urls import url, include
from django.views.static import serve
from django_blog.settings import MEDIA_ROOT
from django.contrib.sitemaps.views import sitemap
from apps.articles.sitemaps import ArticleSitemap
from apps.articles.feeds import AllArticleRssFeed
from django_blog.settings import STATIC_ROOT
# 配置API路由
from rest_framework.routers import DefaultRouter
from django.conf import settings
from apps.api import views as api_views

if settings.API_FLAG:
    router = DefaultRouter()
    router.register(r'users', api_views.UserListSet)
    router.register(r'articles', api_views.ArticleListSet)
    router.register(r'tags', api_views.TagListSet)
    router.register(r'categorys', api_views.CategoryListSet)

sitemaps = {
    'articles': ArticleSitemap,
}

urlpatterns = [
    # path('', xadmin.site.urls),
    url(r'^xadmin_ycl/', xadmin.site.urls),
    # 生产阶段打开
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

    url(r'^blog/', include(('apps.articles.urls', 'articles'), namespace='blog')),


    # url(r'^user/', include(('apps.users.urls', 'users'), namespace='user')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 网站地图
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    # rss订阅
    url(r'^feed/$', AllArticleRssFeed(), name='rss'),
]
if settings.API_FLAG:
    urlpatterns.append(url(r'^api/', include((router.urls, 'api'))))

# 全局404页面配置
handler404 = 'apps.users.views.pag_not_found'
# 全局500页面配置
handler500 = 'apps.users.views.page_error'
# 全局400页面配置
handler400 = 'apps.users.views.no_access'
