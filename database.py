# coding: utf-8
# ------------------------------------------
# 定义penjing项目中，mongodb所用的document文档类；
# 使用MongoEngine ORM模型；抽象层面高于pymongo；
# ------------------------------------------
from mongoengine import *

# Level2 document.
class Dir(EmbeddedDocument):
    article_name = StringField(required=True)
    article_page = StringField(required=True)

# Level1 document.
class Magazine(Document):
    year = StringField(required=True)
    month = StringField(required=True)
    dir = ListField(EmbeddedDocumentField(Dir))
