def to_json(serializer_class, object):
    s = serializer_class(object=object)
    s.validate()
    return s.data
