import pytest


@pytest.fixture
def directives():
    return [
        '@dgraph(type: "Benchmark")',
        "@foo(portfolio_id: $portfolioId)",
        '@search(by: [term]) @dgraph(pred: "film.name")',
    ]
