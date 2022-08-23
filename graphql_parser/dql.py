"""
    This file contains implementation of a parser for translating
    .graphql into pydantic classes
"""
import os
from typing import Tuple, Union
from pyparsing import ParseResults
from jinja2 import Template
from graphql_parser.parsed_schema import (
    DqlParsedQuery,
    DqlParsedUpsert,
)
from graphql_parser.utils import get_replacement_string
from .grammar import dql_query, dql_upsert

SCHEMA_TEMPLATE = (
    f"{os.path.dirname(os.path.realpath(__file__))}/templates/dql_query.html.jinja2"
)
UPSERT_TEMPLATE = (
    f"{os.path.dirname(os.path.realpath(__file__))}/templates/dql_upsert.html.jinja2"
)

PARSED_TYPES = Union[DqlParsedQuery, DqlParsedUpsert]


class DqlParser:
    def __init__(self):
        self.logger = None
        self.types = ["type", "query", "mutation", "upsert"]

    def loads(self, s: str) -> Tuple[PARSED_TYPES, ParseResults]:
        """Loads a string s, s should be a typical dql content and returns a dictionary.

        Note, currently the grammar makes a separation between query (includes query, mutation and upsert)
        and schema type.

        Returns
        ---------
        results: Tuple(dict, pp.ParseResult)
            the resulting dictionary and the raw pp.ParseResult
        """
        object_type = s.split()[0]
        assert object_type in [
            "{",
            "upsert",
        ], f"Error with query while parsing: expected starting with {{ or upsert, got {object_type}"
        d = None
        if object_type == "{":
            # query, mutation types
            d = dql_query.parse_string(s)
            replacement_vars, f_formatted = get_replacement_string(s)
            s = DqlParsedQuery.parse_obj(
                {
                    **d.as_dict(),
                    "raw_string": s,
                    "f_formatted_string": f_formatted,
                    "replacement_vars": replacement_vars,
                }
            )
        elif object_type == "upsert":
            # upsert block
            d = dql_upsert.parse_string(s)
            replacement_vars, f_formatted = get_replacement_string(s)
            s = DqlParsedUpsert.parse_obj(
                {
                    **d.as_dict(),
                    "raw_string": s,
                    "f_formatted_string": f_formatted,
                    "replacement_vars": replacement_vars,
                }
            )
        else:
            # upsert type
            raise NotImplementedError()
        return s, d

    def as_class(self, x: PARSED_TYPES) -> str:
        template = SCHEMA_TEMPLATE if isinstance(x, DqlParsedQuery) else UPSERT_TEMPLATE
        template = Template(open(template, "r").read())
        return template.render({"x": x, "func": get_replacement_string})
