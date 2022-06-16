from django.db import models

# Create your models here.
'''
定义模型类（class）:自定义的模型类必须继承自models.Model，这是django内置的
系统自动会给定义的类添加一个主键-- id
字段 字段名=model.类型（选项），字段其实就是数据表的字段名，字段取名不能与python和mysql内置的关键字

'''

# 定义书类-->在数据库里的表名
class BookInfo(models.Model):
    # id--->系统有自动定义，无须手段定义id
    name = models.CharField(max_length=10, unique=20)
    pub_date = models.DateField(null=True)
    readcount = models.IntegerField(default=0)
    commentcount = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)

    # 修改表名要在类里重新定义一个类，即新表名
    #类的固定写法 class Mete:
    # 表名字的固定写法db_table='表名'
    class Mete:
        db_table='bookinfo'
        verbose_name = '书籍管理' # 即admin

    #重写str方法，让admin显示书籍名字
    def __str__(self):
        return self.name


# 定义人物类
class pepleInfo(models.Model):
    # 性别两种选项值，可定义一个有序字典
    GENDER_CHOICE = (
        (1,'male'),
        (2,'female')
    )
    name = models.CharField(max_length=20, unique=True, verbose_name='姓名')
    gender = models.SmallIntegerField(choices=GENDER_CHOICE, default=1)
    description = models.CharField(max_length=100, null=True)
    is_delete = models.BooleanField(default=False)

    # 外键的约束，读者属于书的下一类，外键约束选 级联CASCADE---->父表中删除或更新对应的行,同时自动的删除或更新自表中匹配的行
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)

    # 修改表名
    class Meta:
        db_table = 'peopleinfo'
        verbose_name = '读者'

        # 重写str方法，让admin显示书籍名字
    def __str__(self):
        return self.name