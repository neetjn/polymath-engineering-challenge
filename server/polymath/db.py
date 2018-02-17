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
    category_level = IntegerField(null=False)
    category_name = TextField()
    category_updated = IntegerField(null=False)
    best_offer_enabled = BooleanField(default=False)
    expired = BooleanField(default=False)
    last_updated = IntegerField(null=False)


def bootstrap(categories):
    created = int(time.time())
    for category in categories.categories:
        Category.create(
            category_id=category.category_id,
            category_parent_id=category.category_parent_id,
            category_level=category.category_level,
            category_name=category.category_name,
            category_updated=categories.update_time,
            best_offer_enabled=category.best_offer_enabled,
            expired=category.expired,
            last_updated=created
        )


def drop_database():
    client.drop_tables([Category])
    client.create_tables([Category])
