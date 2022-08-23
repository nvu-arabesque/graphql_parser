from graphql_parser.utils import format_property


def test_format():
    assert format_property("x!") == "x"
    assert format_property("x") == "Optional[x]"
    assert format_property("[x]") == "Optional[List[Optional[x]]]"
    assert format_property("[x!]") == "Optional[List[x]]"
    assert format_property("[x!]!") == "List[x]"
