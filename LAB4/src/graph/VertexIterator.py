
class VertexIterator:
    """
    Bidirectional-like iterator over vertices (sequence-style).
    Supports: next() via __next__, and reverse iteration via the graph providing __reversed__.
    Holds a reference to graph and a position index.
    """
    def __init__(self, graph, index: int = 0):
        self._g = graph
        self._i = index

    def __iter__(self):
        return self

    def __next__(self):
        if self._i >= self._g.vertex_count():
            raise StopIteration
        val = self._g._vertex_at(self._i)
        self._i += 1
        return val

    # Helper to expose current index for erase-by-iterator
    def index(self):
        return self._i
