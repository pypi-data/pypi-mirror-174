"""
Commonly useful filters for `attr.asdict`.
"""


from ._compat import isclass
from ._make import Attribute


def _split_what(what):
    """
    Returns a tuple of `frozenset`s of classes and attributes.
    """
    return (
        frozenset(cls for cls in what if isclass(cls)),
        frozenset(cls for cls in what if isinstance(cls, Attribute)),
    )


def include(*what):
    """
    Whitelist *what*.

    :param what: What to whitelist.
    :type what: `list` of `type` or `attr.Attribute`\\ s

    :rtype: `callable`
    """
    cls, attrs = _split_what(what)

    def include_(attribute, value):
        return value.__class__ in cls or attribute in attrs

    return include_


def exclude(*what):
    """
    Blacklist *what*.

    :param what: What to blacklist.
    :type what: `list` of classes or `attr.Attribute`\\ s.

    :rtype: `callable`
    """
    cls, attrs = _split_what(what)

    def exclude_(attribute, value):
        return value.__class__ not in cls and attribute not in attrs

    return exclude_
