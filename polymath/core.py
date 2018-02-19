import requests
import time

import os
import xmltodict
from flask_trace import trace
from peewee import fn
from xmler import dict2xml


from polymath.db import Category
from polymath.mediatypes import EBayCategoryDto, EBayCategoriesDto, CategoryDto, CategoryCollectionDto
from polymath.constants import EBAY_API_GATEWAY, EBAY_API_APP_NAME, EBAY_API_CERT_NAME, EBAY_API_COMPATIBILITY_LEVEL, \
    EBAY_API_SITE_ID, EBAY_API_DEV_NAME, EBAY_API_AUTH_TOKEN


ebay_headers = {
    'Content-Type': 'text/xml',
    'X-EBAY-API-CALL-NAME': 'GetCategories',
    'X-EBAY-API-APP-NAME': EBAY_API_APP_NAME,
    'X-EBAY-API-CERT-NAME': EBAY_API_CERT_NAME,
    'X-EBAY-API-DEV-NAME': EBAY_API_DEV_NAME,
    'X-EBAY-API-SITEID': EBAY_API_SITE_ID,
    'X-EBAY-API-COMPATIBILITY-LEVEL': EBAY_API_COMPATIBILITY_LEVEL,
}


def d2xml(body, encoding='utf-8', pretty=False):
    """
    Monkey patch for xmler dict2xml, xmler was designed for Python 2.7
    the encoding it's using doesn't actually work
    """
    return f'<?xml version="1.0" encoding="UTF-8"?>{dict2xml(body)}'


def get_categories_from_ebay():
    """
    Fetch all categories using eBay api.
    Note: This is slightly inefficient the payload is parsed into an ordered dict,
    then into composable objects. This was done to help structure data.

    :returns: EBayCategoriesDto
    """
    request = d2xml({
        'GetCategoriesRequest': {
            '@attrs': { 'xmlns': 'urn:ebay:apis:eBLBaseComponents' },
            'RequesterCredentials': { 'eBayAuthToken': EBAY_API_AUTH_TOKEN },
            'CategorySiteID': '0',
            'DetailLevel': 'ReturnAll',
            'ViewAllNodes': 'true'
        }
    })
    response = requests.post(EBAY_API_GATEWAY, headers=ebay_headers, data=request)

    if response.status_code != 200:
        raise requests.exceptions.BaseHTTPError(f'Expected status code 200, found {response.status_code}')

    payload = xmltodict.parse(response.content)['GetCategoriesResponse']
    updated = int(time.mktime(time.strptime(payload['UpdateTime'][:19], '%Y-%m-%dT%H:%M:%S')))
    return EBayCategoriesDto(
        categories=[EBayCategoryDto(
            category_id=category['CategoryID'],
            category_parent_id=category['CategoryParentID'],
            category_level=category['CategoryLevel'],
            category_name=category['CategoryName'],
            best_offer_enabled=category.get('BestOfferEnabled', False),
            expired=category.get('Expired', False)
        ) for category in payload['CategoryArray']['Category']],
        category_count=payload['CategoryCount'],
        category_version=payload['CategoryVersion'],
        update_time=updated
    )


def get_summary():
    """
    Fetch top level categories from the database.
    """
    # pylint: disable=no-value-for-parameter
    depth = Category.select(fn.Min(Category.category_level)).scalar()
    return CategoryCollectionDto(categories=[category_to_dto(category) \
        for category in Category.select().where(Category.category_level == depth) \
            if not category.expired])


def get_categories():
    """
    Fetch categories from database.
    Note: This method will construct an entire category tree.
    """
    # pylint: disable=no-value-for-parameter
    depth = Category.select(fn.Max(Category.category_level)).scalar()
    categories = [[category_to_dto(category) for category in Category.select()\
        .where(Category.category_level == level + 1) if not category.expired] \
            for level in range(depth)]
    categories.reverse()
    # tree algo, adding children to parent from bottom most level up
    for i, level in enumerate(categories):
        # top level categories have no parent categories
        if i != depth - 1:
            for category in level:
                parent = next(parent for parent in categories[i + 1] \
                    if parent.category_id == category.category_parent_id)
                parent.children.append(category)

    # return the last category which has all of our changes from our tree algo
    return CategoryCollectionDto(categories=categories[-1])


def get_category(category_id, tree=False):
    """
    Fetch category from database.

    :param category_id: Identifier for category to target.
    :type category_id: str
    :param tree: Return entire category tree.
    :type tree: bool
    """
    # pylint: disable=no-value-for-parameter
    category = category_to_dto(Category.get_by_id(category_id))
    category_level = category.category_level
    depth = Category.select(fn.Max(Category.category_level)).scalar()
    levels = [[category_to_dto(category) for category in Category.select()\
        .where(Category.category_level == level + 1) if not category.expired] \
            for level in range(category_level, depth if tree else category_level + 1 )]
    levels.reverse()
    # tree algo, adding children to parent from bottom most level up
    for i, level in enumerate(levels):
        # top level categories have no parent categories
        if level[0].category_level > category_level + 1:
            for c in level:
                parent = next(parent for parent in levels[i + 1] \
                    if parent.category_id == c.category_parent_id)
                parent.children.append(c)
        else:
            break

    if levels:
        # include processed children nodes
        levels[-1] = [l for l in levels[-1] if l.category_parent_id == category.category_id]
        category.children = levels[-1]
    # return the last category which has all of our changes from our tree algo
    return category


def category_to_dto(category):
    """
    Convert database model into data transfer object.

    :param category: Category to convert.
    :type category: Category
    :returns: CategoryDto
    """
    return CategoryDto(
        category_id=category.category_id,
        category_parent_id=category.category_parent_id.category_id \
            if isinstance(category.category_parent_id, Category) else 0,
        category_level=category.category_level,
        category_name=category.category_name,
        category_updated=category.category_updated,
        best_offer_enabled=category.best_offer_enabled,
        expired=category.expired,
        last_updated=category.last_updated
    )


def dto_to_category(category_dto):
    """
    Convert data transfer object into database model.

    :param category_dto: Category data transfer object to convert.
    :type category_dto: CategoryDto
    :returns: Category
    """
    return Category(
        category_id=category_dto.category_id,
        category_parent_id=category_dto.category_parent_id,
        category_level=category_dto.category_level,
        category_name=category_dto.category_name,
        category_updated=category_dto.category_updated,
        best_offer_enabled=category_dto.best_offer_enabled,
        expired=category_dto.expired,
        last_updated=category_dto.last_updated
    )
