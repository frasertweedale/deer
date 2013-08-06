class DeerAttribute(object):
    def __init__(self, type=None, **kwargs):
        self.type = type
        self.has_default = 'default' in kwargs
        self.default = kwargs.get('default')

    def __set__(self, instance, value):
        if self.type and not isinstance(value, self.type):
            raise TypeError
        instance.__elk_attrs__[id(self)] = value

    def __get__(self, instance, owner):
        try:
            return instance.__elk_attrs__[id(self)]
        except KeyError:
            if self.has_default:
                return self.default
            raise AttributeError


class DeerMeta(type):
    def __call__(cls, **kwargs):
        instance = type.__call__(cls)
        instance.__elk_attrs__ = {}

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
