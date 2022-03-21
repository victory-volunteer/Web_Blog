# -*- coding: utf-8 -*-

from haystack import indexes
from apps.articles.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):  # 类名必须为需要检索的Model_name+Index
    text = indexes.CharField(document=True, use_template=True)

    # 其他的字段只是附属的属性，方便调用，在html中也可以使用对象名.object.属性调用
    views = indexes.IntegerField(model_attr='views')  # 重写SearchView时用到了

    # comments = indexes.IntegerField(model_attr='comments')

    # 对那张表进行查询
    def get_model(self):  # 重载get_model方法，必须要有
        # 返回这个model
        return Article

    # 针对哪些数据进行查询
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
