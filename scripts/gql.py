"""
    Tool for generating pydantic from gql definitions
"""
import os
import sys
import logging
import subprocess
from glob import glob

# make sure graphql_parser path is added to python path
sys.path.append(os.getcwd())
from graphql_parser.graphql import GraphqlParser
from graphql_parser.dql import DqlParser

logger = logging.getLogger("__GQL-Generator__")
GQL_DIR = "."
SCHEMA_FILE = "gql_generated_schemas.py"
parser = GraphqlParser()
dql_parser = DqlParser()

file_headers = """
# The content of this file is auto-generated and experimental
# Please do not edit manually and use with caution
from __future__ import annotations

from datetime import datetime
from typing import List, Union, Optional, Dict
from pydantic import BaseModel
"""


def to_pydantic(s: str):
    d, s = parser.loads(s)
    return parser.as_class(d)


def to_pydantic_dql(s: str):
    d, s = dql_parser.loads(s)
    return dql_parser.as_class(d)


if __name__ == "__main__":
    # simple example for now
    logger.info("Started GQL Generation")
    files_pattern = ["**/*.graphql", "**/*.dql"]
    _filenames = (
        glob("**/*.graphql", recursive=True)
        + glob("**/*.gql", recursive=True)
        + glob("**/*.dql", recursive=True)
    )
    filenames = [f"{os.getcwd()}/{x}" for x in _filenames]
    gql_files = [x for x in filenames if x.endswith(".graphql") or x.endswith(".gql")]
    dql_files = [x for x in filenames if x.endswith(".dql")]
    # contents
    gql_contents = [open(x, "r").read() for x in gql_files]
    dql_contents = [open(x, "r").read() for x in dql_files]
    pydantics = [to_pydantic(x) for x in gql_contents]
    dql_pydantics = [to_pydantic_dql(x) for x in dql_contents]
    file_content = "\n".join([file_headers, *pydantics, *dql_pydantics])
    # write to file
    with open(SCHEMA_FILE, "w") as f:
        f.write(file_content)
    # format the code
    subprocess.run(["black", SCHEMA_FILE])
    logger.info("GQL Generation Completed")
