
class CocktailSort:
    """
    Cocktail sort (bidirectional bubble sort).
    API:
        - sort_inplace(seq, key=None, reverse=False) -> None
        - sort(seq, key=None, reverse=False) -> list
    Works with any mutable sequence that supports indexing and assignment.
    """
    @staticmethod
    def sort_inplace(seq, key=None, reverse=False):
        if key is None:
            key = lambda x: x
        n = len(seq)
        if n < 2:
            return
        start = 0
        end = n - 1
        swapped = True
        while swapped:
            swapped = False
            for i in range(start, end):
                if (key(seq[i]) > key(seq[i+1])) ^ reverse:
                    seq[i], seq[i+1] = seq[i+1], seq[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            end -= 1
            for i in range(end-1, start-1, -1):
                if (key(seq[i]) > key(seq[i+1])) ^ reverse:
                    seq[i], seq[i+1] = seq[i+1], seq[i]
                    swapped = True
            start += 1

    @staticmethod
    def sort(seq, key=None, reverse=False):
        seq_copy = list(seq)
        CocktailSort.sort_inplace(seq_copy, key=key, reverse=reverse)
        return seq_copy
