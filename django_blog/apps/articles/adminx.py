import xadmin
from apps.articles.models import Article, Notice, Rotation, FriendLink, BigCategory, Category, Tag, Keyword,CommentUser,Daily_Article


class GlobalSettings(object):
    site_title = '个人博客后台管理系统'
    site_footer = '个人博客'


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class ArticleAdmin(object):
    list_display = ['id', 'title', 'tag_list']


class NoticeAdmin(object):
    pass


class RotationAdmin(object):
    pass


class FriendLinkAdmin(object):
    pass


class BigCategoryAdmin(object):
    pass


class CategoryAdmin(object):
    pass


class TagAdmin(object):
    list_display = ['id', 'name', 'article_list']


class KeywordAdmin(object):
    pass

class CommentUserAdmin(object):
    pass
class Daily_ArticleAdmin(object):
    pass

xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Notice, NoticeAdmin)
xadmin.site.register(Rotation, RotationAdmin)
xadmin.site.register(BigCategory, BigCategoryAdmin)
xadmin.site.register(FriendLink, FriendLinkAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Keyword, KeywordAdmin)
xadmin.site.register(CommentUser, CommentUserAdmin)
xadmin.site.register(Daily_Article, Daily_ArticleAdmin)

xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
