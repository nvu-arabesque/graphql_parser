from numpy import True_
from graphql_parser import grammar


def test_param(param):
    _ = [grammar.param.parse_string(x) for x in param]
    assert True


def test_param_lists(params):
    _ = [grammar.params_list.parse_string(x) for x in params]
    assert True


def test_directives(directives):
    _ = [grammar.gql_directives.parse_string(x) for x in directives]
    assert True


def test_type_header(headers):
    _ = [grammar.gql_type_header.parse_string(x) for x in headers]
    assert True


def test_gql_object(object):
    _ = [grammar.gql_object.parse_string(x) for x in object]
    assert True_


def test_gql_objects(objects_list):
    _ = [grammar.gql_objects_list.parse_string(x) for x in objects_list]
    assert True


def test_query(queries):
    _ = [grammar.query.parse_string(x) for x in queries]
    assert True


def test_schemas(queries):
    _ = [grammar.schema.parse_string(x) for x in queries]
    assert True
