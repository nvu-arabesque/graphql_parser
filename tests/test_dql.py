from graphql_parser.grammar import (
    dql_rdfs_list,
    dql_mutation,
    dql_upsert,
    dql_query_header,
)


def test_rdfs(rdfs):
    _ = [dql_rdfs_list.parse_string(x) for x in rdfs]
    assert True


def test_mutations(dql_mutations):
    _ = [dql_mutation.parse_string(x) for x in dql_mutations]
    assert True


def test_upserts(upserts):
    _ = [dql_upsert.parse_string(x) for x in upserts]
    assert True


def test_dql_query_headers(dql_query_headers):
    _ = [dql_query_header.parse_string(x) for x in dql_query_headers]
    assert True
