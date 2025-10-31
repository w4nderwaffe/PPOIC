
from sorting.CocktailSort import CocktailSort
from sorting.StrandSort import StrandSort
from sorting.Person import Person

from graph.DirectedAdjMatrix import DirectedAdjMatrix
from graph.EdgeIterator import EdgeIterator
from graph.VertexIterator import VertexIterator

def demo_sorting():
    print("=== Task 1: Sorting (Variant 2: Cocktail & Strand) ===")
    arr = [9, 1, 5, 3, 8, 2]
    print("Array before:", arr)
    CocktailSort.sort_inplace(arr)
    print("Array after  (Cocktail):", arr)

    people = [Person("Vlad", 18), Person("Anna", 21), Person("Oleg", 18), Person("Mia", 19)]
    # sort by (age, name)
    sorted_people = StrandSort.sort(people, key=lambda p: (p.age, p.name))
    print("People after (Strand, by age,name):", sorted_people)

def demo_graph():
    print("\n=== Task 2: Directed Graph (Adjacency Matrix) ===")
    g = DirectedAdjMatrix[str]()
    for v in ["A", "B", "C", "D"]:
        g.add_vertex(v)

    g.add_edge(0, 1)  # A->B
    g.add_edge(0, 2)  # A->C
    g.add_edge(1, 2)  # B->C
    g.add_edge(2, 3)  # C->D

    print(g)
    print("vertex_count:", g.vertex_count(), "edge_count:", g.edge_count())
    print("out_degree(A):", g.out_degree(0), "in_degree(C):", g.in_degree(2))

    print("Adjacent from A:", [v for v in g.adj_begin(0)])

    # Erase first edge by iterator
    eit = g.edges_begin()
    first_edge = next(eit)
    g.erase_edge(eit)
    print("After erase first edge:", g, sep="\n")

    # Erase first vertex by iterator (remove 'A')
    vit = g.vertices_begin()
    first_vertex = next(vit)
    g.erase_vertex(vit)  # removes last yielded (A)
    print("After erase first vertex:", g, sep="\n")

if __name__ == "__main__":
    demo_sorting()
    demo_graph()
