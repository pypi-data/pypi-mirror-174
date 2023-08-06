import itertools
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Tuple

INDENT_BLOCK = "  "


class QueryNodeMap:
    def __init__(self):
        self.__counter = itertools.count(start=1)
        self.__map = {}

    def add(self, query_node: "QueryNode") -> int:
        node_id = next(self.__counter)
        self.__map[node_id] = query_node
        return node_id

    def __getitem__(self, node_id: int) -> "QueryNode":
        return self.__map[node_id]


query_node_map = QueryNodeMap()


@dataclass
class NodeRef:
    """
    Used so we can more easily modify the QueryTree by inserting and removing nodes, e.g.
    def subtree_rewrite(subtree_node_ref):
        subtree_node_ref.node = NewNode(subtree_node_ref.node)
    """

    node: "QueryNode"

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.node.columns

    @property
    def inputs(self):
        return self.node.inputs

    def as_str(self, verbose: bool = False) -> str:
        return self.node.as_str(verbose)

    def pretty_print(
        self,
        verbose: bool = False,
        indents: int = 0,
        indent_block: str = INDENT_BLOCK,
        show_ids: bool = True,
        names_only: bool = False,
    ):
        return self.node.pretty_print(verbose, indents, indent_block, show_ids, names_only)


class QueryNode(ABC):
    @property
    @abstractmethod
    def columns(self) -> Tuple[str, ...]:
        """
        The columns in the projectlist coming out of this node.
        """

    def as_ref(self) -> NodeRef:
        return NodeRef(self)

    # used for recursing through the tree for tree rewrites
    @property
    @abstractmethod
    def inputs(self) -> Tuple[NodeRef]:
        pass

    @abstractmethod
    def as_str(self, verbose: bool) -> str:
        """
        Prints contents of this node and calls recursively on its inputs.
        Used by tecton.TectonDataFrame.explain
        """

    def pretty_print_self(
        self,
        verbose: bool = False,
        indents: int = 0,
        indent_block: str = INDENT_BLOCK,
        show_ids: bool = True,
        names_only: bool = False,
    ):
        """
        Returns a formatted string representation of the contents of this node.
        Handles indentation, and optionally generates and displays an id.
        If `names_only` is True, only the class name of the node will be used.
        """
        header = ""
        if show_ids:
            new_id = query_node_map.add(self)
            header = f"<{new_id}>"
        header_length = len(header)

        s = ""

        if names_only:
            s += header
            s += INDENT_BLOCK * indents
            s += self.__class__.__name__
            s += "\n"
            return s

        lines = self.as_str(verbose=verbose).rstrip()
        for i, line in enumerate(lines.split("\n")):
            # We use the header for the first line; for all subsequent lines, we use
            # whitespace of an equal length.
            s += header if i == 0 else " " * header_length
            s += INDENT_BLOCK * indents + line + "\n"
        return s

    def pretty_print(
        self,
        verbose: bool = False,
        indents: int = 0,
        indent_block: str = INDENT_BLOCK,
        show_ids: bool = True,
        names_only: bool = False,
    ) -> str:
        """
        Returns a string representation of the contents of this node and all its ancestors.
        Handles indentation, and optionally generates ids for the node and its ancestors.
        If `names_only` is True, only the class names of the nodes will be used.
        """
        # Build string representation of this node.
        s = self.pretty_print_self(verbose, indents, indent_block, show_ids, names_only)

        # Recursively add ancestors.
        for i in self.inputs:
            s += i.pretty_print(verbose, indents + 1, indent_block, show_ids, names_only)

        return s
