
class InIncidentIterator:
    """
    Bidirectional-like iterator over edges incoming to a vertex v.
    Yields (from, v) index pairs.
    """
    def __init__(self, graph, v_index: int, start_from=0):
        self._g = graph
        self._v = v_index
        self._frm = start_from
        self._advance()

    def __iter__(self):
        return self

    def __next__(self):
        if self._frm >= self._g.vertex_count():
            raise StopIteration
        current = (self._frm, self._v)
        self._frm += 1
        self._advance()
        return current

    def _advance(self):
        n = self._g.vertex_count()
        while self._frm < n and not self._g._has_edge(self._frm, self._v):
            self._frm += 1
