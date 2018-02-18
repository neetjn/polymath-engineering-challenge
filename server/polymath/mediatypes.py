from r2dto import fields, Serializer


class EBayCategoryDto(object):
    def __init__(self, **kwargs):
        self.category_id = kwargs.get('category_id', 0)
        self.category_parent_id = kwargs.get('category_parent_id', 0)
        self.category_level = kwargs.get('category_level', 0)
        self.category_name = kwargs.get('category_name', 0)
        self.best_offer_enabled = kwargs.get('best_offer_enabled', False)
        self.expired = kwargs.get('expired', False)


class EBayCategoriesDto(object):
    def __init__(self, **kwargs):
        self.categories = kwargs.get('categories', [])
        self.category_count = kwargs.get('category_count', 0)
        self.category_version = kwargs.get('category_version', 0)
        self.update_time = kwargs.get('update_time', 0)


class LinkDto(object):
    def __init__(self, href=None, rel=None):
        self.href = href
        self.rel = rel


class LinkDtoSerializer(Serializer):
    href = fields.StringField()
    rel = fields.StringField()

    class Meta(object):
        model = LinkDto


class CategoryDto(object):
    def __init__(self, **kwargs):
        self.links = []
        self.category_id = kwargs.get('category_id', 0)
        self.category_parent_id = kwargs.get('category_parent_id', 0)
        self.category_level = kwargs.get('category_level', 0)
        self.category_name = kwargs.get('category_name', 0)
        self.category_updated = kwargs.get('category_updated', 0)
        self.children = kwargs.get('children', [])
        self.best_offer_enabled = kwargs.get('best_offer_enabled', False)
        self.expired = kwargs.get('expired', False)
        self.last_updated = kwargs.get('last_updated', 0)


class BaseCategorySerializer(Serializer):
    links = fields.ListField(fields.ObjectField(LinkDtoSerializer))
    category_id = fields.IntegerField(name='categoryId')
    category_parent_id = fields.IntegerField(name='categoryParentId')
    category_level = fields.IntegerField(name='categoryLevel')
    category_name = fields.IntegerField(name='categoryName')
    category_updated = fields.IntegerField(name='categoryUpdated')
    best_offer_enabled = fields.BooleanField(name='bestOffersEnabled')
    expired = fields.BooleanField()
    last_updated = fields.IntegerField(name='lastUpdated')

    class Meta(object):
        model = CategoryDto


class CategoryDtoSerializer(BaseCategorySerializer):
    children = fields.ListField(fields.ObjectField(BaseCategorySerializer))
