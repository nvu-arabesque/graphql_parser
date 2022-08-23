import pytest


@pytest.fixture
def rdfs():
    return [
        """
        uid(p) <Portfolio.transactions> * .
        uid(v) <PortfolioTransaction.date> * .
        uid(v) <PortfolioTransaction.assetid> * .
        uid(v) <PortfolioTransaction.description> * .
        uid(v) <PortfolioTransaction.cash> * .
        uid(v) <PortfolioTransaction.currency> * .
        """,
        """
        a <b> c .
        a <b> c .
        """,
    ]
