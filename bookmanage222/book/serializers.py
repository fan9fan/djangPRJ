'''
# drf框架 序列化和反序列化
序列化器用处：
将对象数据转换成字典

'''

from rest_framework import serializers
#  定义书本模型对应的对象序列化器
class BookInfoSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    pub_date = serializers.DateField
    readcount = serializers.IntegerField()


# 定义人物模型对应的对象序列化器
class PeopleInfoSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    password = serializers.CharField()
    description = serializers.CharField()
    is_delete = serializers.BooleanField()

    book_id = serializers.IntegerField()