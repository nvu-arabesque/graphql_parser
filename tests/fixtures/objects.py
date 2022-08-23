import pytest


@pytest.fixture
def objects_list():
    return [
        """
  getPortfolio(size: size) {
      portfolioid
      nav
  },
  getNav(size: size) {
      date
      nav
  }
  """
    ]
