from dataclasses import replace
import re
from typing import List

# a lookup table for type conversions from graphql to python. Note
# only for primitvies type
PRIMITIVES_GRAPHQL_PYTHON = {
    "DateTime": "datetime",
    "String": "str",
    "Float": "float",
    "Int": "int",
    "Boolean": "bool",
}


def format_property(property: str):
    """Returns a formatted type of a property of a graphql type.

    This function is intended to pass to the jinja template for tidyness
    instead of using native jinja2.

    The rule for this format is:
        - endswith ! is mandatory, without is optional
        - surrounded by [] indicates a list
    """
    _content = re.search("\[(.*?)\]", property)
    content = None if _content is None else _content.groups()[0]
    # inner list type
    if content is not None:
        is_optional = content.endswith("!")
        _inner = content.replace("!", "")
        _inner = (
            PRIMITIVES_GRAPHQL_PYTHON[_inner]
            if _inner in PRIMITIVES_GRAPHQL_PYTHON
            else _inner
        )
        inner = f"List[{_inner}]" if is_optional else f"List[Optional[{_inner}]]"
    else:
        inner = property
    # outer layer is optional
    is_optional = property.endswith("!")
    # strip off the outer optional
    outer = inner.replace("!", "")
    outer = (
        PRIMITIVES_GRAPHQL_PYTHON[outer]
        if outer in PRIMITIVES_GRAPHQL_PYTHON
        else outer
    )
    # dealing with outer optional type, bit hard to follow
    return outer if property.endswith("!") else f"Optional[{outer}]"


def get_replacement_string(s: str) -> List[str]:
    """gather all replacement variables inside the object.

    A replacement variable is one starts with $.
    """
    # alpha numeric and underscores
    pattern = "\$([a-zA-Z0-9_]*)"
    search = re.search(pattern, s)
    result = search.groups() if search is not None else None
    replaced = re.sub(pattern, r"{\1}", s)
    return result, replaced
