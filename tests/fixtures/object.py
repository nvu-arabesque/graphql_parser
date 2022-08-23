import pytest


@pytest.fixture
def object():
    return [
        """
    getPortfolio(size: size) {
        portfolioid
        nav
    }""",
        """
    getPortfolio {
        id
        nav
    }
        """,
    ]
