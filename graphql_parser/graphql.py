"""
    This file contains implementation of a parser for translating
    .graphql into pydantic classes
"""
import os
from pydantic import BaseModel
from typing import Tuple, Union
from pyparsing import ParseResults
from jinja2 import Template
from graphql_parser.parsed_schema import (
    GraphqlParsedQuery,
    GraphqlParsedSchema,
)
from graphql_parser.utils import format_property
from .grammar import query, schema
from enum import Enum


class SupportedGQLType(Enum):
    SCHEMA = "type"
    QUERY = "query"
    MUTATION = "mutation"
    UPSERT = "upsert"


TEMPLATE = f"{os.path.dirname(os.path.realpath(__file__))}/templates/schema.html.jinja2"
ParsedTypes = Union[GraphqlParsedSchema, GraphqlParsedQuery]


class GraphqlParser:
    def __init__(self):
        self.logger = None
        self.types = ["type", "query", "mutation", "upsert"]

    def loads(self, s: str) -> Tuple[ParsedTypes, ParseResults]:
        """Loads a string s, s should be a typical graphql content and returns a dictionary.

        Note, currently the grammar makes a separation between query (includes query, mutation and upsert)
        and schema type.

        Returns
        ---------
        results: Tuple(dict, pp.ParseResult)
            the resulting dictionary and the raw pp.ParseResult
        """
        object_type = s.strip().split(" ")[0]
        assert (
            object_type in self.types
        ), f"Error with type definition: expected one of {self.types}, got {object_type}"
        d = None
        if SupportedGQLType(object_type) == SupportedGQLType.SCHEMA:
            d = schema.parse_string(s)
            s = GraphqlParsedSchema.parse_obj(d.as_dict())
        else:
            d = query.parse_string(s)
        return s, d

    def as_class(self, x: ParsedTypes) -> str:
        template = Template(open(TEMPLATE, "r").read())
        return template.render({"x": x, "format": format_property})
