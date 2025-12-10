class CocktailSort:
    """
    Cocktail sort (bidirectional bubble sort).

    Объектный вариант:
      - key и reverse задаются в конструкторе
      - sort_inplace(self, seq) сортирует последовательность на месте
      - sort(self, seq) возвращает новый отсортированный список
    """

    def __init__(self, key=None, reverse: bool = False):
        # key — функция извлечения ключа сортировки
        # reverse — если True, сортировка по убыванию
        self.key = key if key is not None else (lambda x: x)
        self.reverse = reverse

    def sort_inplace(self, seq):
        """
        Сортирует последовательность на месте алгоритмом Cocktail sort.
        Работает с любым изменяемым индексируемым контейнером (например, list).
        """
        n = len(seq)
        if n < 2:
            return

        key = self.key
        reverse = self.reverse

        start = 0
        end = n - 1
        swapped = True

        while swapped:
            swapped = False

            # Проход слева направо
            for i in range(start, end):
                if (key(seq[i]) > key(seq[i + 1])) ^ reverse:
                    seq[i], seq[i + 1] = seq[i + 1], seq[i]
                    swapped = True

            if not swapped:
                break

            swapped = False
            end -= 1

            # Проход справа налево
            for i in range(end - 1, start - 1, -1):
                if (key(seq[i]) > key(seq[i + 1])) ^ reverse:
                    seq[i], seq[i + 1] = seq[i + 1], seq[i]
                    swapped = True

            start += 1

    def sort(self, seq):
        """
        Возвращает новый отсортированный список, не изменяя исходную последовательность.
        """
        seq_copy = list(seq)
        self.sort_inplace(seq_copy)
        return seq_copy
