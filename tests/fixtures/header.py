import pytest


@pytest.fixture
def headers():
    return [
        "query GetPortfolio($portfolioId: String!, $getPortfolioPortfolioId2: String!)",
        "query GetPortfolio @dgraph($portfolioId: String!, $getPortfolioPortfolioId2: String!)",
        'type Benchmark @dgraph(type: "Benchmark")',
        "mutation Test($post: [AddPostInput!]!)",
        "type Post",
    ]
