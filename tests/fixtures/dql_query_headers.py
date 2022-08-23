import pytest


@pytest.fixture
def dql_query_headers():
    return [
        "estQuery(func: eq(Portfolio.portfolioId, $portfolioId))",
        "estQuery(func: eq(Portfolio.portfolioId, $portfolioId)) @filter(name, 'test')",
    ]
