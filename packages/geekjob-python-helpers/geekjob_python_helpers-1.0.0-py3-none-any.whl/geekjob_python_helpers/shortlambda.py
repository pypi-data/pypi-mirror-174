class ShortLambda:
    """
    Short lambda realisation
    """

    def __ne__(self, obj) -> callable[[object], bool]: return lambda x: x != obj

    def __eq__(self, obj) -> callable[[object], bool]: return lambda x: x == obj

    def __gt__(self, obj) -> callable[[object], bool]: return lambda x: x > obj

    def __ge__(self, obj) -> callable[[object], bool]: return lambda x: x >= obj

    def __lt__(self, obj) -> callable[[object], bool]: return lambda x: x < obj

    def __le__(self, obj) -> callable[[object], bool]: return lambda x: x <= obj


class X(ShortLambda):
    """
    Alias for ShortLambda class
    """
    ...
