
class EdgeIterator:
    """
    Bidirectional-like iterator over all edges (u -> v).
    Yields (u_index, v_index) as a tuple, similar to std::pair.
    Exposes _last to support erase by iterator.
    """
    def __init__(self, graph, start_u=0, start_v=0):
        self._g = graph
        self._u = start_u
        self._v = start_v
        self._last = None
        self._advance_to_edge()

    def __iter__(self):
        return self

    def __next__(self):
        if self._u >= self._g.vertex_count():
            raise StopIteration
        current = (self._u, self._v)
        self._last = current
        self._step_forward()
        return current

    # Internal helpers
    def _advance_to_edge(self):
        n = self._g.vertex_count()
        while self._u < n:
            while self._v < n:
                if self._g._has_edge(self._u, self._v):
                    return
                self._v += 1
            self._u += 1
            self._v = 0

    def _step_forward(self):
        n = self._g.vertex_count()
        self._v += 1
        if self._v >= n:
            self._u += 1
            self._v = 0
        self._advance_to_edge()
