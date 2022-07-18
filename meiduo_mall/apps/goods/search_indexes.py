from haystack import indexes
from apps.goods.models import SKU

'''
create search_indexes.py file within the app
索引类比类继承自indexes.SearchIndex, indexes.Indexable
必须定义一个字段 document=True
    字段名可以随意取，取名 text 只是习惯而已
 use_template=True --->允许我们设定一个单独的文件来指定字段检索
 
create a new template inside your template directory called search/indexes/myapp/note_text.txt

定义好索引后运行 python3 manage.py rebuild_index 将得到搜索的模型
'''

class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return SKU

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

