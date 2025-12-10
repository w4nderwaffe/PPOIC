class StrandSort:
    """
    Strand sort — сортировка на основе выделения возрастающих подпоследовательностей
    и их последующего слияния.

    Объектный вариант:
      - key и reverse задаются в конструкторе
      - sort(self, seq) возвращает новый отсортированный список
      - sort_inplace(self, seq) заменяет содержимое списка отсортированным
    """

    def __init__(self, key=None, reverse: bool = False):
        self.key = key if key is not None else (lambda x: x)
        self.reverse = reverse

    def _merge(self, a, b):
        """
        Сливает два отсортированных списка a и b в один отсортированный.
        Учитывает key и reverse из состояния объекта.
        """
        res = []
        i = j = 0
        key = self.key
        reverse = self.reverse

        while i < len(a) and j < len(b):
            cond = key(a[i]) <= key(b[j])
            if reverse:
                cond = not cond

            if cond:
                res.append(a[i])
                i += 1
            else:
                res.append(b[j])
                j += 1

        if i < len(a):
            res.extend(a[i:])
        if j < len(b):
            res.extend(b[j:])

        return res

    def sort(self, seq):
        """
        Возвращает новый список, отсортированный алгоритмом Strand sort.
        Исходная последовательность не изменяется.
        """
        key = self.key
        reverse = self.reverse
        v = list(seq)

        if len(v) < 2:
            return v

        output = []

        while v:
            # Формируем одну возрастающую подпоследовательность (strand)
            strand = [v.pop(0)]
            i = 0
            while i < len(v):
                if (key(v[i]) >= key(strand[-1])) ^ reverse:
                    strand.append(v.pop(i))
                else:
                    i += 1

            # Сливаем полученный strand с текущим результатом
            output = self._merge(output, strand)

        return output

    def sort_inplace(self, seq):
        """
        Сортирует изменяемую последовательность (список) на месте.
        """
        sorted_list = self.sort(seq)
        seq[:] = sorted_list
