import datetime
import json
import time
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

from polymath.constants import DB_NAME


client = SqliteExtDatabase(DB_NAME)
client.connect()


class SqliteModel(Model):
    class Meta(object):
        database = client


class Category(SqliteModel):
#CategoryID, CategoryName, CategoryLevel, BestOfferEnabled, CategoryParentID
    category_id = PrimaryKeyField(null=False)
    category_parent_id = ForeignKeyField('self', null=True, backref='children')
    category_name = TextField()
    best_offer_enabled = BooleanField(default=False)
    expired = BooleanField(default=False)
    last_updated = DateTimeField()


def bootstrap(categories):
    for category in categories.categories:
        Category.create(
            category_id=category.category_id,
            category_parent_id=category.category_parent_id,
            category_level=category.category_level,
            category_name=category.category_name,
            best_offer_enabled=category.best_offer_enabled,
            expired=category.expired
        )


def drop_database():
    client.drop_tables([Category])
    client.create_tables([Category])
