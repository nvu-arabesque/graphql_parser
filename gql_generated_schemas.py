# The content of this file is auto-generated and experimental
# Please do not edit manually and use with caution
from __future__ import annotations

from datetime import datetime
from typing import List, Union, Optional, Dict
from pydantic import BaseModel


class User(BaseModel):
    displayName: Optional[str]
    email: Optional[str]
    emailVerified: Optional[bool]
    photoURL: Optional[str]
    roles: Optional[List[str]]
    userId: str
    _directives: Optional[Dict] = {"@dgraph": [{"key": "type", "value": '"User"'}]}


class TestQueryDqlUpsert:
    def __init__(self, **kwargs):
        self.kwargs = None
        self.replacement_vars = ["portfolioId"]
        self.query: str = """TestQuery eq(Portfolio.portfolioId: {portfolioId})  @filter(foo(bar, "bar")) AND @filter(foo(bar, "bar2")) { p as uid
Portfolio.transactions   { v as uid } }"""
        self.mutations: Dict = [
            {
                "type": "delete",
                "rdfs": [
                    "uid(p) <Portfolio.transactions> * .",
                    "uid(v) <PortfolioTransaction.date> * .",
                    "uid(v) <PortfolioTransaction.assetid> * .",
                    "uid(v) <PortfolioTransaction.description> * .",
                    "uid(v) <PortfolioTransaction.cash> * .",
                    "uid(v) <PortfolioTransaction.currency> * .",
                ],
            },
            {
                "type": "delete",
                "rdfs": [
                    "uid(p) <Portfolio.transactions> * .",
                    "uid(v) <PortfolioTransaction.date> * .",
                    "uid(v) <PortfolioTransaction.assetid> * .",
                    "uid(v) <PortfolioTransaction.description> * .",
                    "uid(v) <PortfolioTransaction.cash> * .",
                    "uid(v) <PortfolioTransaction.currency> * .",
                ],
            },
        ]

    def query(self):
        return self.raw_str.format(**self.kwargs)
