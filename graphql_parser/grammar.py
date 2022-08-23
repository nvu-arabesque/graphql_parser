"""
    This file contains the language definition for parser
    Credit the content of this file is adapted from https://github.com/lsmag/graphql-python/blob/master/graphql/grammar.py
    It would be nice to find the grammar for dgraph,
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pyparsing as pp

# ========================================================
# Define grammar
# ========================================================

# -------------- tokens -----------------
OPEN_BRACE = pp.Suppress("{")
CLOSE_BRACE = pp.Suppress("}")
OPEN_PAREN = pp.Suppress("(")
CLOSE_PAREN = pp.Suppress(")")
COMMA = pp.Suppress(",")
COLON = pp.Suppress(":")
DOT = pp.Suppress(".")
EOF = pp.Suppress(pp.LineEnd())
OPEN_ANGLE = pp.Suppress("<")
CLOSE_ANGLE = pp.Suppress(">")

# types
# not supressing square brack
OPEN_SQUARE_BRAC = pp.Literal("[")
CLOSE_SQUARE_BRAC = pp.Literal("]")
singular_types = pp.Word(pp.alphanums) + pp.Optional(pp.Literal("!"))
list_types = pp.Combine(
    OPEN_SQUARE_BRAC + singular_types + CLOSE_SQUARE_BRAC + pp.Optional(pp.Literal("!"))
)
# identifier
identifier = pp.Regex(r"[\$]?[a-zA-Z_.][a-zA-Z0-9_./]*").setName("identifier")
string = pp.Regex(r"[\$]?[a-zA-Z_.][a-zA-Z0-9_./]*")
number = pp.Regex(r"-?\d+(\.\d+)?").setName("number")
variables = pp.Word("$" + pp.alphas, pp.alphanums + "!")
literal = pp.Combine(
    number
    | variables
    | string
    | pp.quoted_string
    | singular_types
    | list_types
    | "null"
    | "true"
    | "false"
).setName("literal")

param = pp.Group(
    identifier.setResultsName("key") + COLON + literal.setResultsName("value")
).setName("param")
param_pairs_list = param + pp.ZeroOrMore(COMMA + param)
params_list = OPEN_PAREN + pp.Optional(param_pairs_list) + CLOSE_PAREN

filter_param = pp.Group(identifier + params_list).setName("filter param")

# ============================================================
#           GQL Grammar
# ============================================================
# --------------------- gql directives -----------------
gql_directive_identifier = pp.Regex(r"@[a-zA-Z_][a-zA-Z0-9_/]*").setName("directive")
gql_directive = pp.Group(
    gql_directive_identifier.setResultsName("type")
    + pp.Optional(params_list).setResultsName("params")
)
gql_directives = gql_directive + pp.ZeroOrMore(gql_directive)


# -------------------- type def  header -----------------
def is_type(t):
    return t[0] in ["type", "query", "mutation", "upsert"]


gql_typedef = pp.Regex(r"\b[A-Za-z]+\b").addCondition(is_type)

gql_type_header = (
    gql_typedef.setResultsName("type")
    + identifier.setResultsName("identifier")
    + pp.Optional(pp.Group(params_list).setResultsName("params"))
    + pp.Optional(gql_directives).setResultsName("directives")
)

# --------- header --------------
gql_header = (
    identifier.setResultsName("name")
    + pp.Optional(pp.Group(params_list).setResultsName("params"))
    + pp.Optional(pp.Group(pp.ZeroOrMore(DOT + filter_param)).setResultsName("filters"))
)

# defining the gql object
# --------- gql object --------------
gql_object = pp.Forward()

gql_property = pp.Group(gql_object) | (identifier + pp.Optional(gql_directives))
gql_properties_list = gql_property + pp.ZeroOrMore(gql_property)
gql_object << (
    pp.Group(gql_header).setResultsName("header")
    + OPEN_BRACE
    + pp.Group(gql_properties_list).setResultsName("properties")
    + CLOSE_BRACE
)

gql_objects_list = pp.Group(gql_object) + pp.ZeroOrMore(pp.Group(gql_object))
# ------- query -------------------
query = (
    pp.Suppress(pp.LineStart())
    + gql_type_header
    + OPEN_BRACE
    + gql_objects_list.setResultsName("gql_objects")
    + CLOSE_BRACE
    + EOF
)
# -------- schema -------------------
# note this can be merged in with query, but for some reasons i thought separating them is better
gql_type_definition = pp.Group(
    identifier.setResultsName("key")
    + COLON
    + literal.setResultsName("value")
    + pp.Optional(gql_directives)
).setName("param")
gql_type_definition_list = gql_type_definition + pp.ZeroOrMore(gql_type_definition)
schema = (
    pp.Suppress(pp.LineStart())
    + gql_type_header
    + OPEN_BRACE
    + gql_type_definition_list.setResultsName("properties")
    + CLOSE_BRACE
    + EOF
)
# ============================================================
#           DQL Grammar: DQL slightly diffrent from GQL
# see e.g. https://dgraph.io/docs/query-language/connecting-filters/
# ============================================================
dql_literal = pp.Combine(
    number
    | string
    | variables
    | pp.quoted_string
    | singular_types
    | list_types
    | "null"
    | "true"
    | "false"
).setName("literal")
connectives = pp.Literal("AND") | pp.Literal("OR") | pp.Literal("NOT")
#  ----- dql edge filter -----------------------
dql_filter = pp.Group(
    pp.Optional(connectives).setResultsName("connectives")
    + identifier.setResultsName("function")
    + OPEN_PAREN
    + dql_literal.setResultsName("variable")
    + pp.Optional(COMMA + dql_literal.setResultsName("value"))
    + CLOSE_PAREN
).setName("dql filter")
dql_filters_list = dql_filter + pp.ZeroOrMore(dql_filter)
dql_edge_filter = (
    pp.Suppress("@filter")
    + OPEN_PAREN
    + dql_filters_list.setResultsName("filters")
    + CLOSE_PAREN
)
# ------- dql function  and header -------------------------
dql_function = OPEN_PAREN + pp.Suppress("func") + COLON + dql_filter + CLOSE_PAREN
dql_query_header = (
    identifier.setResultsName("identifier")
    + pp.Optional(dql_function).setResultsName("function")
    + pp.Optional(dql_edge_filter).setResultsName("filters")
)
# --------- dql objects -------------------------------------
dql_object = pp.Forward()
dql_prop = pp.Combine(
    identifier + pp.Optional(pp.Literal("as") + dql_literal),
    join_string=" ",
    adjacent=False,
)
dql_property = pp.Group(dql_object) | dql_prop
dql_properties_list = dql_property + pp.ZeroOrMore(dql_property)
dql_object << (
    pp.Group(dql_query_header).setResultsName("header")
    + OPEN_BRACE
    + pp.Group(dql_properties_list).setResultsName("properties")
    + CLOSE_BRACE
)
dql_query = pp.Suppress(OPEN_BRACE) + dql_object + pp.Suppress(CLOSE_BRACE)


# --------------dql mutation --------------------------------
# dql mutation consists of rdfs
dql_op = pp.Literal("set") | pp.Literal("delete")
dql_object = pp.Regex(r"[a-zA-Z_][a-zA-Z0-9_.\(\)/]*").setName("dql_object")
dql_predicate = pp.Combine((OPEN_ANGLE + identifier + CLOSE_ANGLE)).setName("predicate")
dql_subject = variables | pp.Literal("*")
dql_rdf = pp.Group(
    dql_object.setResultsName("object")
    + dql_predicate.setResultsName("predicate")
    + dql_subject.setResultsName("subject")
    + DOT
)
dql_rdfs_list = dql_rdf + pp.ZeroOrMore(dql_rdf)
dql_mutation = pp.Group(
    OPEN_BRACE
    + dql_op.setResultsName("function")
    + OPEN_BRACE
    + dql_rdfs_list.setResultsName("rdfs")
    + CLOSE_BRACE
    + CLOSE_BRACE
)
# -------------- upsert block ------------------------------
# an upsert block consists of exactly one query block and
# a list of fragments and mutations block
dql_upsert_query_block = pp.Group(
    pp.Suppress(pp.Literal("query")) + dql_query
).setResultsName("query")
dql_upsert_mutation_block = pp.Suppress(pp.Literal("mutation")) + dql_mutation
dql_upsert_mutations_list = dql_upsert_mutation_block + pp.ZeroOrMore(
    dql_upsert_mutation_block
)
dql_upsert = (
    pp.Suppress(pp.LineStart())
    + pp.Literal("upsert")
    + OPEN_BRACE
    + dql_upsert_query_block
    + dql_upsert_mutations_list.setResultsName("mutations")
    + CLOSE_BRACE
    + EOF
)
