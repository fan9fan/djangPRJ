from django.db import models

# Create your models here.
'''
定义模型类（class）:自定义的模型类必须继承自models.Model，这是django内置的
系统自动会给定义的类添加一个主键-- id
字段 字段名=model.类型（选项），字段其实就是数据表的字段名，字段取名不能与python和mysql内置的关键字

'''

# 定义书类
class BookInfo(models.Model):
    # id--->系统有自动定义，无须手段定义id
    name = models.CharField(max_length=10)
    #重写str方法，让admin显示书籍名字
    def __str__(self):
        return self.name


# 定义人物类
class pepleInfo(models.Model):
    name = models.CharField(max_length=10)
    gender = models.BooleanField()
    # 外键的约束，人物属于哪本书
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)