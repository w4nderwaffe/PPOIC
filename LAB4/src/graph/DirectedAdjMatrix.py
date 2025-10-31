
from typing import Generic, TypeVar, List, Iterable, Tuple
from .GraphError import GraphError
from .VertexIterator import VertexIterator
from .EdgeIterator import EdgeIterator
from .OutIncidentIterator import OutIncidentIterator
from .InIncidentIterator import InIncidentIterator
from .AdjacentIterator import AdjacentIterator

T = TypeVar("T")

class DirectedAdjMatrix(Generic[T]):
    """
    Oriented (directed) graph with adjacency matrix.
    The underlying representation is hidden behind API and iterators.
    STL-like surface with Pythonic idioms.
    """

    # typedef-like aliases (STL spirit; Python doesn't have pointers/const)
    value_type = object
    reference = object
    const_reference = object
    pointer = object
    const_pointer = object

    def __init__(self) -> None:
        self._vertices: List[T] = []
        self._adj: List[List[bool]] = []  # adj[i][j] = True if edge i->j

    # copy/assignment/destructor semantics (Pythonic)
    def __copy__(self):
        g = DirectedAdjMatrix[T]()
        g._vertices = list(self._vertices)
        g._adj = [row[:] for row in self._adj]
        return g

    def __deepcopy__(self, memo):
        from copy import deepcopy
        g = DirectedAdjMatrix[T]()
        g._vertices = deepcopy(self._vertices, memo)
        g._adj = deepcopy(self._adj, memo)
        return g

    def __del__(self):
        # not strictly needed in Python, present to mirror 'destructor' requirement
        pass

    # --- Basic state ---
    def empty(self) -> bool:
        return len(self._vertices) == 0

    def clear(self) -> None:
        self._vertices.clear()
        self._adj.clear()

    # --- Comparisons (by vertices then edges) ---
    def __eq__(self, other) -> bool:
        if not isinstance(other, DirectedAdjMatrix):
            return NotImplemented
        return self._vertices == other._vertices and self._adj == other._adj

    def __lt__(self, other) -> bool:
        if not isinstance(other, DirectedAdjMatrix):
            return NotImplemented
        if self._vertices != other._vertices:
            return self._vertices < other._vertices
        return self._adj < other._adj

    def __le__(self, other): return self == other or self < other
    def __gt__(self, other): return not (self <= other)
    def __ge__(self, other): return not (self < other)

    # --- Core API ---
    def vertex_count(self) -> int:
        return len(self._vertices)

    def edge_count(self) -> int:
        return sum(1 for i in range(self.vertex_count()) for j in range(self.vertex_count()) if self._adj[i][j])

    def add_vertex(self, value: T) -> None:
        self._vertices.append(value)
        n = len(self._vertices)
        for row in self._adj:
            row.append(False)
        self._adj.append([False] * n)

    def remove_vertex(self, index: int) -> None:
        self._check_vertex(index)
        self._vertices.pop(index)
        self._adj.pop(index)
        for row in self._adj:
            row.pop(index)

    def has_vertex(self, value: T) -> bool:
        return value in self._vertices

    def add_edge(self, i: int, j: int) -> None:
        self._check_vertex(i); self._check_vertex(j)
        if i == j:
            raise GraphError("Self-loop disallowed by policy")
        self._adj[i][j] = True

    def remove_edge(self, i: int, j: int) -> None:
        self._check_vertex(i); self._check_vertex(j)
        self._adj[i][j] = False

    def has_edge(self, i: int, j: int) -> bool:
        self._check_vertex(i); self._check_vertex(j)
        return self._adj[i][j]

    # degrees
    def out_degree(self, i: int) -> int:
        self._check_vertex(i)
        return sum(1 for b in self._adj[i] if b)

    def in_degree(self, j: int) -> int:
        self._check_vertex(j)
        return sum(1 for row in self._adj if row[j])

    # --- Iterators ---
    # vertices
    def vertices_begin(self) -> VertexIterator:
        return VertexIterator(self, 0)

    def vertices_end(self) -> VertexIterator:
        return VertexIterator(self, self.vertex_count())

    def __iter__(self):
        # default iteration over vertices' values
        return self.vertices_begin()

    def __reversed__(self):
        # reverse iteration over vertices' values
        for i in range(self.vertex_count() - 1, -1, -1):
            yield self._vertex_at(i)

    # edges
    def edges_begin(self) -> EdgeIterator:
        return EdgeIterator(self, 0, 0)

    def edges_end(self) -> EdgeIterator:
        return EdgeIterator(self, self.vertex_count(), 0)

    def edges(self):
        return self.edges_begin()

    # reverse variants for all iterator families (Pythonic generators)
    def vertices_reverse(self):
        for i in range(self.vertex_count()-1, -1, -1):
            yield self._vertex_at(i)

    def edges_reverse(self):
        for i in range(self.vertex_count()-1, -1, -1):
            for j in range(self.vertex_count()-1, -1, -1):
                if self._adj[i][j]:
                    yield (i, j)

    def out_reverse(self, v: int):
        self._check_vertex(v)
        for j in range(self.vertex_count()-1, -1, -1):
            if self._adj[v][j]:
                yield (v, j)

    def in_reverse(self, v: int):
        self._check_vertex(v)
        for i in range(self.vertex_count()-1, -1, -1):
            if self._adj[i][v]:
                yield (i, v)

    def adj_reverse(self, v: int):
        self._check_vertex(v)
        for j in range(self.vertex_count()-1, -1, -1):
            if self._adj[v][j]:
                yield self._vertex_at(j)

    # incident edges / adjacent vertices
    def out_begin(self, v: int) -> OutIncidentIterator:
        self._check_vertex(v)
        return OutIncidentIterator(self, v, 0)

    def out_end(self, v: int) -> OutIncidentIterator:
        self._check_vertex(v)
        return OutIncidentIterator(self, v, self.vertex_count())

    def in_begin(self, v: int) -> InIncidentIterator:
        self._check_vertex(v)
        return InIncidentIterator(self, v, 0)

    def in_end(self, v: int) -> InIncidentIterator:
        self._check_vertex(v)
        return InIncidentIterator(self, v, self.vertex_count())

    def adj_begin(self, v: int) -> AdjacentIterator:
        self._check_vertex(v)
        return AdjacentIterator(self, v, 0)

    def adj_end(self, v: int) -> AdjacentIterator:
        self._check_vertex(v)
        return AdjacentIterator(self, v, self.vertex_count())

    # erase by iterator-like handles
    def erase_vertex(self, iterator: VertexIterator) -> None:
        idx = iterator._i if hasattr(iterator, "_i") else None
        if idx is None or idx <= 0:
            # when erase after consuming next, iterator points to element AFTER the one returned
            # adjust to remove previous element
            idx = 0
        else:
            idx -= 1
        if idx >= self.vertex_count():
            raise GraphError("Iterator out of range for erase_vertex")
        self.remove_vertex(idx)

    def erase_edge(self, iterator: EdgeIterator) -> None:
        # EdgeIterator yields next edge on __next__, so we cannot directly access "current".
        # Provide a helper that erases the last yielded edge if iterator exposes last.
        if not hasattr(iterator, "_last"):
            raise GraphError("Iterator does not expose last yielded edge for erase")
        u, v = iterator._last
        self.remove_edge(u, v)

    # --- Output ---
    def __str__(self) -> str:
        parts = []
        parts.append(f"Vertices ({self.vertex_count()}): " + " ".join(f"[{v}]" for v in self._vertices))
        edges = []
        for i in range(self.vertex_count()):
            for j in range(self.vertex_count()):
                if self._adj[i][j]:
                    edges.append(f"({self._vertices[i]}->{self._vertices[j]})")
        parts.append("Edges (" + str(len(edges)) + "): " + " ".join(edges))
        return "\n".join(parts)

    # --- Internal helpers (representation hidden from outside users) ---
    def _check_vertex(self, i: int) -> None:
        if not (0 <= i < len(self._vertices)):
            raise GraphError("Vertex index out of range")

    def _has_edge(self, i: int, j: int) -> bool:
        return self._adj[i][j]

    def _vertex_at(self, i: int) -> T:
        return self._vertices[i]
