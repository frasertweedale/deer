class DeerAttribute(object):
    def __init__(self, type=None, **kwargs):
        self.type = type
        self.has_default = 'default' in kwargs
        self.default = kwargs.get('default')


    def __get__(self, instance, owner):
        if not hasattr(instance, '__deer_attrs__'):
            instance.__deer_attrs__ = {}
        try:
            return instance.__deer_attrs__[id(self)]
        except KeyError:
            if self.has_default:
                return self.default
            raise AttributeError


    def __set__(self, instance, value):
        if not hasattr(instance, '__deer_attrs__'):
            instance.__deer_attrs__ = {}
        if self.type is not None and not isinstance(value, self.type):
            raise TypeError
        instance.__deer_attrs__[id(self)] = value


class DeerMeta(type):
    def __call__(cls, **kwargs):
        instance = type.__call__(cls)

        deer_attrs = {
            k: v for k, v in cls.__dict__.items()
            if isinstance(v, DeerAttribute)
        }
        for name, attr in deer_attrs.viewitems():
            if name in kwargs:
                setattr(instance, name, kwargs[name])

        return instance


class Deer(object):
    __metaclass__ = DeerMeta
