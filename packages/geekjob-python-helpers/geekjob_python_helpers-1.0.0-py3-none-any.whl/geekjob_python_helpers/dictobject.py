class StdClass(dict):
    """
    PHP like stdClass
    Can be used as a dict or as an object
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class DictObject(dict):
    """
    Class for storing data in dict
    """

    # def __init__(self, *args, **kwargs):
    #     super(DictObject, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """
        Return string representation of dict
        """
        # return [f for f in dir(self) if not callable(getattr(self, f))]
        return self.__dict__


def obj(d: dict) -> DictObject:
    """
    Convert dict to DictObject
    """
    for k in d:
        if isinstance(d[k], dict):
            d[k] = obj(d[k])

    return type("DictObject", (DictObject,), d)


def convert_class_to_dict(obj: callable, prefix: str | None = None) -> dict:
    """
    Convert class to dict
    """
    if prefix is None:
        prefix = obj().__class__.__name__.upper() + "_"
    return {
        prefix + k.upper(): v
        for k, v in obj.__dict__.items()
        if not k.startswith("_")
    }
