from unittest import TestCase

from polymath.core import get_categories_from_ebay, get_category, get_categories, get_summary
from polymath.db import bootstrap, drop_database


"""
Could have mocked the request to eBay, for a less volatile test environment, didn't have enough time.
These tests are only validating dtos constructed by the project core, nothing else.
"""

drop_database()
categories = get_categories_from_ebay()
bootstrap(categories)


class CoreTest(TestCase):

    def setUp(self):
        self.category_id = 888

    def test_get_summary(self):
        category_summary = get_summary()
        self.assertEqual(len(category_summary.categories), 34)
        for category in category_summary.categories:
            self.assertEqual(category.category_level, 1)
            self.assertFalse(category.expired)
            self.assertEqual(len(category.children), 0)

    def test_get_shallow_category(self):
        """ensure shallow categories are constructed as intended"""
        category = get_category(self.category_id)
        self.assertEqual(len(category.children), 14)
        self.assertEqual(category.category_id, self.category_id)
        self.assertEqual(category.category_parent_id, self.category_id)
        self.assertEqual(category.category_level, 1)
        self.assertFalse(category.expired)
        for child in category.children:
            self.assertEqual(child.category_parent_id, self.category_id)
            self.assertEqual(len(child.children), 0)
            self.assertFalse(child.expired)

    def test_get_category_tree(self):
        """ensure category trees are constructed as intended"""
        category = get_category(self.category_id, True)
        self.assertEqual(len(category.children), 14)
        self.assertEqual(category.category_id, self.category_id)
        self.assertEqual(category.category_parent_id, self.category_id)
        self.assertEqual(category.category_level, 1)
        self.assertFalse(category.expired)
        for child in category.children:
            self.assertEqual(child.category_parent_id, self.category_id)
            self.assertFalse(child.expired)
        self.assertEqual(len(category.children[1].children), 15)
