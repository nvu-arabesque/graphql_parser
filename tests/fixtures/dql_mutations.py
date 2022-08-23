import pytest


@pytest.fixture
def dql_mutations():
    return [
        """
        {
            delete {
                uid(p) <Portfolio.transactions> * .
                uid(v) <PortfolioTransaction.date> * .
                uid(v) <PortfolioTransaction.assetid> * .
                uid(v) <PortfolioTransaction.description> * .
                uid(v) <PortfolioTransaction.cash> * .
                uid(v) <PortfolioTransaction.currency> * .
            }
        }
        """,
        """
        {
            set {
                a <b> * .
                a <b> c .
                uid(v) <PortfolioTransaction.assetid> * .
                uid(v) <PortfolioTransaction.description> * .
                uid(v) <PortfolioTransaction.cash> * .
                uid(v) <PortfolioTransaction.currency> * .
            }
        }
        """,
    ]
