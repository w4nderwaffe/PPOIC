import copy
import pytest

from src.graph.DirectedAdjMatrix import DirectedAdjMatrix
from src.graph.GraphError import GraphError


def make_simple_graph():
    """
    Вспомогательный граф:
        A -> B
        A -> C
        B -> C
        C -> D
    """
    g = DirectedAdjMatrix[str]()
    for v in ["A", "B", "C", "D"]:
        g.add_vertex(v)

    g.add_edge(0, 1)  # A->B
    g.add_edge(0, 2)  # A->C
    g.add_edge(1, 2)  # B->C
    g.add_edge(2, 3)  # C->D
    return g


def test_add_vertex_and_counts():
    g = DirectedAdjMatrix[int]()
    assert g.empty() is True
    g.add_vertex(10)
    g.add_vertex(20)
    g.add_vertex(30)
    assert g.vertex_count() == 3
    assert g.edge_count() == 0
    assert g.empty() is False
    assert g.has_vertex(20) is True
    assert g.has_vertex(99) is False


def test_add_and_has_edge():
    g = DirectedAdjMatrix[str]()
    for v in ["A", "B", "C"]:
        g.add_vertex(v)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    assert g.has_edge(0, 1) is True
    assert g.has_edge(1, 2) is True
    assert g.has_edge(0, 2) is False
    assert g.edge_count() == 2


def test_remove_edge_and_vertex():
    g = make_simple_graph()
    # было 4 ребра
    assert g.edge_count() == 4
    g.remove_edge(0, 1)
    assert g.edge_count() == 3
    assert g.has_edge(0, 1) is False

    # удалим вершину B (index=1)
    g.remove_vertex(1)
    # теперь вершины: [A, C, D]
    assert g.vertex_count() == 3
    # рёбра пересчитались, конкретную структуру можно проверить строкой
    s = str(g)
    # в оставшемся графе должны быть вершины A, C, D:
    assert "Vertices (3): [A] [C] [D]" in s


def test_degrees():
    g = make_simple_graph()
    # A->B, A->C, B->C, C->D
    assert g.out_degree(0) == 2  # A
    assert g.out_degree(1) == 1  # B
    assert g.out_degree(2) == 1  # C
    assert g.in_degree(2) == 2   # C (из A и B)
    assert g.in_degree(0) == 0   # A


def test_vertices_iteration():
    g = make_simple_graph()
    vs = list(g)  # __iter__ -> vertices_begin -> values
    assert vs == ["A", "B", "C", "D"]

    rev_vs = list(reversed(g))
    assert rev_vs == ["D", "C", "B", "A"]


def test_edges_iteration():
    g = make_simple_graph()
    edges = list(g.edges_begin())
    # Порядок: по i от 0..n-1, по j от 0..n-1
    # A->B (0,1), A->C (0,2), B->C (1,2), C->D (2,3)
    assert edges == [(0, 1), (0, 2), (1, 2), (2, 3)]


def test_adjacent_iterator():
    g = make_simple_graph()
    # соседи A: B, C
    adj_from_a = list(g.adj_begin(0))
    assert adj_from_a == ["B", "C"]


def test_in_out_incident_iterators():
    g = make_simple_graph()
    # исходящие из A
    out_a = list(g.out_begin(0))
    assert out_a == [(0, 1), (0, 2)]

    # входящие в C
    in_c = list(g.in_begin(2))
    # в C идут из A(0) и B(1)
    assert in_c == [(0, 2), (1, 2)]


def test_reverse_helpers():
    g = make_simple_graph()
    # vertices_reverse
    rev_vertices = list(g.vertices_reverse())
    assert rev_vertices == ["D", "C", "B", "A"]

    # edges_reverse — перебор рёбер в обратном порядке индексов
    rev_edges = list(g.edges_reverse())
    assert len(rev_edges) == 4

    # out_reverse(A)
    out_rev_a = list(g.out_reverse(0))
    # из A идут в B и C, но порядок обратный по индексам -> (0,2), (0,1)
    assert out_rev_a == [(0, 2), (0, 1)]

    # in_reverse(C)
    in_rev_c = list(g.in_reverse(2))
    # в C входят из A(0) и B(1); по обратному порядку индексов -> (1,2), (0,2)
    assert in_rev_c == [(1, 2), (0, 2)]

    # adj_reverse(A)
    adj_rev_a = list(g.adj_reverse(0))
    assert adj_rev_a == ["C", "B"]


def test_erase_edge_by_iterator():
    g = make_simple_graph()
    eit = g.edges_begin()
    first_edge = next(eit)
    assert first_edge == (0, 1)
    g.erase_edge(eit)
    # A->B должно исчезнуть
    assert g.has_edge(0, 1) is False
    assert g.edge_count() == 3


def test_erase_vertex_by_iterator():
    g = make_simple_graph()
    vit = g.vertices_begin()
    first_vertex_value = next(vit)
    assert first_vertex_value == "A"
    g.erase_vertex(vit)  # удалит A
    # теперь первая вершина должна быть B (бывший index=1)
    vs = list(g)
    assert vs[0] == "B"
    assert g.vertex_count() == 3


def test_graph_error_on_bad_vertex_index():
    g = DirectedAdjMatrix[int]()
    g.add_vertex(1)
    with pytest.raises(GraphError):
        g.add_edge(0, 5)  # неправильный индекс вершины

    with pytest.raises(GraphError):
        g.out_degree(10)

    with pytest.raises(GraphError):
        g.in_degree(-1)


def test_graph_error_on_self_loop():
    g = DirectedAdjMatrix[int]()
    g.add_vertex(1)
    with pytest.raises(GraphError):
        g.add_edge(0, 0)  # self-loop запрещён


def test_clear_and_empty():
    g = make_simple_graph()
    assert g.empty() is False
    g.clear()
    assert g.empty() is True
    assert g.vertex_count() == 0
    assert g.edge_count() == 0


# ---- ДОП. ТЕСТЫ ДЛЯ ПОДНЯТИЯ ПОКРЫТИЯ ----

def test_graph_copy_and_str():
    g = DirectedAdjMatrix[int]()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(0, 1)

    g_shallow = copy.copy(g)
    g_deep = copy.deepcopy(g)

    # проверяем, что копии содержат те же данные
    assert g_shallow._vertices == g._vertices
    assert g_deep._vertices == g._vertices
    assert g_shallow.edge_count() == g.edge_count()
    assert g_deep.edge_count() == g.edge_count()

    s = str(g)
    assert "Vertices" in s
    assert "Edges" in s


def test_iterators_end_positions():
    g = DirectedAdjMatrix[str]()
    for v in ["A", "B"]:
        g.add_vertex(v)
    g.add_edge(0, 1)

    # vertices_end
    vit_end = g.vertices_end()
    with pytest.raises(StopIteration):
        next(vit_end)

    # edges_end
    eit_end = g.edges_end()
    with pytest.raises(StopIteration):
        next(eit_end)

    # in/out/adj end итераторы
    with pytest.raises(StopIteration):
        next(g.out_end(0))
    with pytest.raises(StopIteration):
        next(g.in_end(0))
    with pytest.raises(StopIteration):
        next(g.adj_end(0))


def test_erase_edge_error():
    g = DirectedAdjMatrix[int]()
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(0, 1)

    class FakeIterator:
        """Итератор без _last, чтобы спровоцировать ошибку в erase_edge."""
        pass

    fake = FakeIterator()
    with pytest.raises(GraphError):
        g.erase_edge(fake)


def test_graph_comparisons():
    g1 = DirectedAdjMatrix[int]()
    g2 = DirectedAdjMatrix[int]()
    for v in [1, 2]:
        g1.add_vertex(v)
        g2.add_vertex(v)
    g1.add_edge(0, 1)
    g2.add_edge(0, 1)

    # равны
    assert g1 == g2
    assert not (g1 != g2)
    assert not (g1 < g2)
    assert not (g1 > g2)
    assert g1 <= g2
    assert g1 >= g2

    # добавим ребро в g2, сравнения поменяются
    g2.add_vertex(3)
    # по вершинам уже не равны, поэтому порядок по спискам вершин
    assert g1 != g2