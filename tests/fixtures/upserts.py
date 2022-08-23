import pytest


@pytest.fixture
def upserts():
    return [
        """
        upsert {
            query {
                TestQuery(func: eq(Portfolio.portfolioId, $portfolioId)) {
                    p as uid
                    Portfolio.transactions {
                    v as uid
                }
            }
        }

        mutation {
            delete {
                uid(p) <Portfolio.transactions> * .
                uid(v) <PortfolioTransaction.date> * .
                uid(v) <PortfolioTransaction.assetid> * .
                uid(v) <PortfolioTransaction.description> * .
                uid(v) <PortfolioTransaction.cash> * .
                uid(v) <PortfolioTransaction.currency> * .
                }
            }
        }
        """
    ]
