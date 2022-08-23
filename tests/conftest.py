"""
    This file contains configs for running test
"""
import logging

from .fixtures.directives import directives
from .fixtures.header import headers
from .fixtures.object import object
from .fixtures.objects import objects_list
from .fixtures.param import param
from .fixtures.params import params
from .fixtures.queries import queries
from .fixtures.dql_mutations import dql_mutations
from .fixtures.rdfs import rdfs
from .fixtures.upserts import upserts
from .fixtures.dql_query_headers import dql_query_headers

logger = logging.getLogger("__Test__")
