import pytest


@pytest.fixture
def schemas():
    return [
        """
        type Benchmark @dgraph(type: "Benchmark") {
            benchmarkId: String! @id
            nav: [PortfolioNavData!]
            currency: String!
            holdings: [PortfolioAssetHolding!]
        }
        """,
        """
        type Post {
            postID: String! @id
            title: String! @search(by: [term, fulltext])
            text: String @search(by: [fulltext, term])
            author: Author!
        }
        """,
    ]
