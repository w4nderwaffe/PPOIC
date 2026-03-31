
class OutIncidentIterator:
    """
    Bidirectional-like iterator over edges outgoing from a vertex v.
    Yields (v, to) index pairs.
    """
    def __init__(self, graph, v_index: int, start_to=0):
        self._g = graph
        self._v = v_index
        self._to = start_to
        self._advance()

    def __iter__(self):
        return self

    def __next__(self):
        if self._to >= self._g.vertex_count():
            raise StopIteration
        current = (self._v, self._to)
        self._to += 1
        self._advance()
        return current

    def _advance(self):
        n = self._g.vertex_count()
        while self._to < n and not self._g._has_edge(self._v, self._to):
            self._to += 1
