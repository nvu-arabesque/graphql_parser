import pytest


@pytest.fixture
def params():
    return [
        "(size: size, size: 123, portfolio: $portfolioId), (size: size, size: 123, $portfolio: [String]!)"
    ]
