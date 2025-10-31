
from copy import copy, deepcopy
import pytest
from src.graph.DirectedAdjMatrix import DirectedAdjMatrix
from src.graph.GraphError import GraphError

def build_graph():
    g = DirectedAdjMatrix[str]()
    for v in ["A","B","C","D"]:
        g.add_vertex(v)
    g.add_edge(0,1) # A->B
    g.add_edge(0,2) # A->C
    g.add_edge(1,2) # B->C
    g.add_edge(2,3) # C->D
    return g

def test_basic_counts_and_has():
    g = build_graph()
    assert g.vertex_count() == 4
    assert g.edge_count() == 4
    assert g.has_vertex("A")
    assert g.has_edge(0,1)
    assert not g.has_edge(1,0)

def test_degrees():
    g = build_graph()
    assert g.out_degree(0) == 2
    assert g.in_degree(2) == 2

def test_iter_vertices_and_reverse():
    g = build_graph()
    assert [v for v in g] == ["A","B","C","D"]
    assert list(reversed(g)) == ["D","C","B","A"]
    assert list(g.vertices_reverse()) == ["D","C","B","A"]

def test_iter_edges_and_reverse():
    g = build_graph()
    edges = list(g.edges())
    assert (0,1) in edges and (2,3) in edges
    rev = list(g.edges_reverse())
    assert (2,3) in rev and (0,1) in rev

def test_incident_and_adjacent_and_reverse():
    g = build_graph()
    outA = list(g.out_begin(0))
    assert (0,1) in outA and (0,2) in outA
    inC = list(g.in_begin(2))
    assert (0,2) in inC and (1,2) in inC
    adjA = list(g.adj_begin(0))
    assert adjA == ["B","C"]
    assert list(g.out_reverse(0)) == [(0,2),(0,1)]
    assert list(g.in_reverse(2)) == [(1,2),(0,2)]
    assert list(g.adj_reverse(0)) == ["C","B"]

def test_erase_by_iterators_and_remove_vertex():
    g = build_graph()
    eit = g.edges_begin()
    first = next(eit)
    g.erase_edge(eit)  # erases last yielded
    assert g.edge_count() == 3

    vit = g.vertices_begin()
    first_v = next(vit)
    g.erase_vertex(vit)  # removes 'A'
    assert g.vertex_count() == 3
    # After removing A, ensure indices updated and graph still valid
    assert not g.has_vertex("A")

def test_comparisons_and_copy():
    g1 = build_graph()
    g2 = build_graph()
    assert g1 == g2
    cp = copy(g1)
    dp = deepcopy(g1)
    assert cp == g1 and dp == g1
    # remove edge to change ordering
    g2.remove_edge(0,1)
    assert g1 != g2
    assert (g2 < g1) or (g1 < g2)  # strict ordering defined

def test_exceptions():
    g = DirectedAdjMatrix[int]()
    g.add_vertex(1)
    with pytest.raises(GraphError):
        g.add_edge(0,0)  # self loop not allowed
    with pytest.raises(GraphError):
        g.remove_vertex(5)
    with pytest.raises(GraphError):
        g.has_edge(0,5)
    with pytest.raises(GraphError):
        g.out_begin(2)
