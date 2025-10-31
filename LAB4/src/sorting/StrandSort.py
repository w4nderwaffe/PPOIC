
class StrandSort:
    """
    Strand sort.
    API:
        - sort(seq, key=None, reverse=False) -> list
        - sort_inplace(seq, key=None, reverse=False) -> None (replaces contents of list)
    Works for sequences; returns a new sorted list. For in-place, pass a list.
    """
    @staticmethod
    def _merge(a, b, key, reverse):
        res = []
        i = j = 0
        while i < len(a) and j < len(b):
            cond = (key(a[i]) <= key(b[j]))
            if reverse:
                cond = not cond
            if cond:
                res.append(a[i]); i += 1
            else:
                res.append(b[j]); j += 1
        if i < len(a): res.extend(a[i:])
        if j < len(b): res.extend(b[j:])
        return res

    @staticmethod
    def sort(seq, key=None, reverse=False):
        if key is None:
            key = lambda x: x
        v = list(seq)
        if len(v) < 2:
            return v
        output = []
        while v:
            strand = [v.pop(0)]
            i = 0
            while i < len(v):
                if (key(v[i]) >= key(strand[-1])) ^ reverse:
                    strand.append(v.pop(i))
                else:
                    i += 1
            output = StrandSort._merge(output, strand, key, reverse)
        return output

    @staticmethod
    def sort_inplace(seq, key=None, reverse=False):
        sorted_list = StrandSort.sort(seq, key=key, reverse=reverse)
        # replace contents in place if possible
        if hasattr(seq, '__setitem__') and hasattr(seq, '__delitem__'):
            seq[:] = sorted_list
        else:
            raise TypeError("sort_inplace requires a mutable sequence (like list).")
