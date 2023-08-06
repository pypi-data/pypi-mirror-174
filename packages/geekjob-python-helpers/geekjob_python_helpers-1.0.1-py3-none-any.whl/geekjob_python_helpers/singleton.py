def singleton(clas):
    """
    Decorator to make a class a singleton.
    """
    instances = {}

    def getinstance(*args, **kwargs):
        """
        Get an instance of the singleton.
        """
        if clas not in instances:
            instances[clas] = clas(*args, **kwargs)
        return instances[clas]

    return getinstance
