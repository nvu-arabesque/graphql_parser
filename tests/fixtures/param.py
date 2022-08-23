import pytest


@pytest.fixture
def param():
    return [
        "size: size",
        "size: 123",
        "portfolio: $portfolioId",
        "portfolio: $portfolioId)",
        "$portfolio: [String]",
        "$portfolio: [String!]",
        "$portfolio: [String!]!",
    ]
