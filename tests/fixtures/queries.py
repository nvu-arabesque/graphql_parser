import pytest


@pytest.fixture
def queries():
    return [
        """
query GetPortfolio($portfolioId: String!, $getPortfolioPortfolioId2: String!) {
  GetPortfolioNav(portfolio_id: $portfolioId) {
    portfolio_id
    nav {
      data {
        date
        nav
      }
    }
  }
  GetPortfolio(portfolioId: $getPortfolioPortfolioId2) {
    nav {
      data {
        dates
      }
    }
  }
}
    """,
    ]
