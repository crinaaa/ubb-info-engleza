import random

class Graph:
    def __init__(self, vertices_number = 0):
        self._vertices = set(range(vertices_number))
        self._edges = {}  # (x,y) -> cost
        self._inbound_edges = {i: set() for i in range(vertices_number)}
        self._outbound_edges = {i: set() for i in range(vertices_number)}


    def nr_vertices(self):
        """
        O(1) complexity
        :return: number of vertices in the graph
        """
        return len(self._vertices)

    def nr_edges(self):
        """
        O(1) complexity
        :return: the number of edges in the graph
        """
        return len(self._edges)

    def vertices(self):
        """
        Iterator over all vertex ids.
        Returns a copy of the graph, so that the caller cannot modify the graph.
        O(n) to iterate
        :return:
        """
        return iter(self._vertices)

    def has_vertex(self, x:int):
        """
        Check if vertex x exists in the graph.
        O(1) complexity
        :param x: wanted vertex
        """
        return x in self._vertices

    def is_edge(self, x:int, y:int):
        """
        O(1) complexity
        :param x: first vertex
        :param y: second vertex
        :return: True is the pair (x,y) exists, False otherwise
        """
        return (x,y) in self._edges

    def get_edges(self):
        """
        Iterator over all (x,y) pairs which form edges.
        :return: a copy of the dictionary keys, so that the caller cannot modify the graph
        """
        return iter(list(self._edges.keys()))

    def get_cost_of_edge(self, x:int, y:int):
        """
        O(1) complexity
        :param x: first vertex
        :param y: second vertex
        :return: the cost of the edge (x,y)
        """
        if (x,y) not in self._edges:
            raise ValueError(f"Edge {x,y} does not exist!")
        return self._edges[(x,y)]

    def set_cost_of_edge(self, x:int, y:int, new_value:int):
        """
        O(1) complexity
        :param x: first vertex
        :param y: second vertex
        :param new_value: new cost of the edge
        """
        if (x,y) not in self._edges:
            raise ValueError(f"Edge {x,y} does not exist!")
        self._edges[(x,y)] = new_value

    def get_in_degree(self, x:int):
        """
        O(1) complexity - len() is O(1) on sets
        :param x: given vertex
        :return: the in degree of vertex x
        """
        if x not in self._vertices:
            raise ValueError(f"Vertex {x} does not exist!")
        return len(self._inbound_edges[x])

    def get_out_degree(self, x:int):
        """
        O(1) complexity - len() is O(1) on sets
        :param x: given vertex
        :return: the in degree of vertex x
        """
        if x not in self._vertices:
            raise ValueError(f"Vertex {x} does not exist!")
        return len(self._outbound_edges[x])

    def in_edges(self, x:int):
        """
        Iterator over the source vertices of inbound edges to x.
        Returns a copy (list) — O(deg) to build, O(1) per step.
        """
        if x not in self._vertices:
            raise ValueError(f"Vertex {x} does not exist!")
        return iter(list(self._inbound_edges[x]))

    def out_edges(self, x: int):
        """
        Iterator over the source vertices of outbound edges from x.
        Returns a copy (list) — O(deg) to build, O(1) per step.
        """
        if x not in self._vertices:
            raise ValueError(f"Vertex {x} does not exist!")
        return iter(list(self._outbound_edges[x]))

    def add_edge(self, x:int, y:int, cost:int):
        """
        O(1) complexity on average
        :param x: first vertex
        :param y: second vertex
        :param cost: cost of the edge (x,y)
        """
        if x not in self._vertices:
            raise ValueError(f"Vertex {x} does not exist!")
        if y not in self._vertices:
            raise ValueError(f"Vertex {y} does not exist!")
        if (x,y) in self._edges:
            raise ValueError(f"Edge {x,y} already exists!")
        self._edges[(x,y)] = cost
        self._inbound_edges[y].add(x)
        self._outbound_edges[x].add(y)

    def remove_edge(self, x:int, y:int):
        """
        O(1) on average
        :param x: first vertex
        :param y: second vertex
        """
        if x not in self._vertices:
            raise ValueError(f"Vertex {x} does not exist!")
        if y not in self._vertices:
            raise ValueError(f"Vertex {y} does not exist!")
        if (x,y) not in self._edges:
            raise ValueError(f"Edge {x,y} does not exist!")
        del self._edges[(x,y)]
        self._outbound_edges[x].discard(y)
        self._inbound_edges[y].discard(x)


    def add_vertex(self, x:int):
        """
        O(1) on average
        :param x: vertex to add
        """
        if x in self._vertices:
            raise ValueError(f"Vertex {x} already exists!")
        self._vertices.add(x)
        self._inbound_edges[x] = set()
        self._outbound_edges[x] = set()

    def remove_vertex(self, x:int):
        """
        O(1) on average
        :param x: vertex to remove
        """
        if x not in self._vertices:
            raise ValueError(f"Vertex {x} does not exist!")

        #remove outbound edges from x
        for y in list(self._outbound_edges[x]):
            del self._edges[(x,y)]
            self._inbound_edges[y].discard(x)

        #remove inbound edges to x
        for y in list(self._inbound_edges[x]):
            del self._edges[(y,x)]
            self._outbound_edges[y].discard(x)

        del self._outbound_edges[x]
        del self._inbound_edges[x]
        self._vertices.discard(x)

    def copy(self):
        """
        Returns a fully independent deep copy of this graph
        """
        new_graph = Graph()
        new_graph._vertices = set(self._vertices)
        new_graph._edges = dict(self._edges)
        new_graph._outbound_edges = {k: set(v) for k, v in self._outbound_edges.items()}
        new_graph._inbound_edges = {k: set(v) for k, v in self._inbound_edges.items()}
        return new_graph


def generate_random_graph(vertices_number: int, edges_number: int):
    max_edges = vertices_number * (vertices_number - 1)
    if edges_number > max_edges:
        raise ValueError("Too many edges.")

    graph = Graph(vertices_number)
    added = 0
    while added < edges_number:
        x = random.randint(0, vertices_number - 1)
        y = random.randint(0, vertices_number - 1)
        if x != y and not graph.is_edge(x, y):
            graph.add_edge(x, y, random.randint(0, 1000))
            added += 1
    return graph