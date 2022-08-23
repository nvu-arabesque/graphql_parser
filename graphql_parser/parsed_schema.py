from __future__ import annotations
import textwrap
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, root_validator, validator


class GraphqlDirective(BaseModel):
    type: str
    params: Optional[List[dict]]


class GraphqlProperties(BaseModel):
    key: str
    value: str
    directives: Optional[List[GraphqlDirective]]


class GraphqlParsedSchema(BaseModel):
    type: str
    identifier: str
    properties: List[GraphqlProperties]
    directives: Optional[List[GraphqlDirective]]


class GraphqlParsedQuery(BaseModel):
    type: str
    identifier: str
    objects: List[str]
    directives: Optional[GraphqlDirective]


class DqlFunction(BaseModel):
    function: str
    variable: str
    value: str
    string: Optional[str]

    @root_validator(pre=False)
    def _set_string(cls, values: dict) -> dict:
        values["string"] = "{}({}: {})".format(
            values["function"], values["variable"], values["value"]
        )
        return values


class DqlFilter(BaseModel):
    function: str
    variable: str
    value: str
    connectives: Optional[str]
    string: Optional[str]

    @root_validator(pre=False)
    def _set_string(cls, values: dict) -> dict:
        _connectives = values["connectives"]
        connectives = f"{_connectives}" if _connectives is not None else ""
        values["string"] = "{} @filter({}({}, {}))".format(
            connectives, values["function"], values["variable"], values["value"]
        )
        return values


class DqlHeader(BaseModel):
    identifier: str
    function: Optional[List[DqlFunction]]
    filters: Optional[List[DqlFilter]]
    string: Optional[str]

    @root_validator(pre=False)
    def _set_string(cls, values: dict) -> dict:
        filters_s = (
            " ".join([x.string for x in values["filters"]])
            if values["filters"] is not None
            else ""
        )
        function_s = (
            " ".join([x.string for x in values["function"]])
            if values["function"] is not None
            else ""
        )
        values["string"] = "{} {} {}".format(
            values["identifier"], function_s, filters_s
        )
        return values


class DqlParsedQuery(BaseModel):
    header: DqlHeader
    properties: Optional[List[Union[str, DqlParsedQuery]]]
    raw_string: Optional[str]
    f_formatted_string: Optional[str]
    replacement_vars: Optional[List[str]]

    @root_validator(pre=False)
    def _set_string(cls, values: dict) -> dict:
        header_s = values["header"].string
        properties_s = (
            "\n".join(
                [
                    x.string if isinstance(x, DqlParsedQuery) else x
                    for x in values["properties"]
                ]
            )
            if values["properties"] is not None
            else ""
        )
        values["string"] = f"{header_s} {{ {properties_s} }}"
        return values


class DqlRdf(BaseModel):
    object: str
    predicate: str
    subject: str
    string: Optional[str]

    @root_validator(pre=False)
    def _set_string(cls, values: dict) -> dict:
        object = values["object"]
        predicate = values["predicate"]
        subject = values["subject"]
        values["string"] = f"{object} <{predicate}> {subject} ."
        return values


class DqlMutation(BaseModel):
    function: str
    rdfs: List[DqlRdf]
    string: Optional[str]

    @root_validator(pre=False)
    def _set_string(cls, values: dict) -> dict:
        _rdfs = values["rdfs"]
        rdfs = "\n".join([x.string for x in _rdfs])
        function = values["function"]
        values["string"] = f"{function} {{ {rdfs} }} "
        return values


class DqlParsedUpsert(BaseModel):
    query: DqlParsedQuery
    mutations: List[DqlMutation]
    # should inherit
    raw_string: Optional[str]
    f_formatted_string: Optional[str]
    replacement_vars: Optional[List[str]]
    # TODO
    fragments: Optional[str] = None


DqlParsedQuery.update_forward_refs()
