# cf. <https://rdflib.readthedocs.io/en/stable/_modules/rdflib/collection.html>

from __future__ import annotations

from rdflib import Graph
from rdflib.term import Node


class List(object):
    def __init__(self, graph: Graph, node: Node, content: list[Node] | None,
            accept_singleton: bool = False):
        pass

