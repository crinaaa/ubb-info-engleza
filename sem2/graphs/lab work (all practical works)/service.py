from domain import Graph, generate_random_graph


class GraphService:
    def __init__(self):
        self._graph = Graph()

    def read_graph(self, filename: str):
        try:
            with open(filename, "r") as f:
                v, e = f.readline().split()
                v, e = int(v), int(e)
                self._graph = Graph(v)
                for _ in range(e):
                    x, y, cost = f.readline().split()
                    self._graph.add_edge(int(x), int(y), int(cost))
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found.")
        except PermissionError:
            raise PermissionError(f"No permission to read '{filename}'.")

    # def write_graph(self, filename: str):
    #     try:
    #         with open(filename, "w") as f:
    #             f.write(f"{self._graph.nr_vertices()} {self._graph.nr_edges()}\n")
    #             for x, y in self._graph.get_edges():
    #                 cost = self._graph.get_cost_of_edge(x, y)
    #                 f.write(f"{x} {y} {cost}\n")
    #     except PermissionError:
    #         raise PermissionError(f"No permission to write '{filename}'.")

    def write_graph(self, filename: str):
        try:
            # sorted list used for the mapping
            sorted_vertices = sorted(self._graph.vertices())
            # old_id -> new_id  (e.g. {0:0, 2:1, 5:2, ...})
            remap = {old: new for new, old in enumerate(sorted_vertices)}

            with open(filename, "w") as f:
                f.write(f"{self._graph.nr_vertices()} {self._graph.nr_edges()}\n")
                for x, y in self._graph.get_edges():
                    cost = self._graph.get_cost_of_edge(x, y)
                    f.write(f"{remap[x]} {remap[y]} {cost}\n")
        except PermissionError:
            raise PermissionError(f"No permission to write '{filename}'.")

    def generate_random(self, vertices_number:int, edges_number:int):
        self._graph = generate_random_graph(vertices_number, edges_number)

    def generate_and_save(self, vertices_number: int, edges_number: int, filename: str):
        """Generate a random graph and save it to a file."""
        self._graph = generate_random_graph(vertices_number, edges_number)
        self.write_graph(filename)

    def no_of_vertices(self):
        return self._graph.nr_vertices()

    def no_of_edges(self):
        return self._graph.nr_edges()

    def get_vertices(self):
        return self._graph.vertices()

    def check_edge(self, x:int, y:int):
        return self._graph.is_edge(x, y)

    def cost_of_edge(self, x:int, y:int):
        if not self._graph.is_edge(x, y):
            raise ValueError("The edge does not exist!")
        return self._graph.get_cost_of_edge(x,y)

    def set_new_cost(self, x:int, y:int, cost:int):
        if not self._graph.is_edge(x, y):
            raise ValueError("Invalid edge!")
        self._graph.set_cost_of_edge(x,y,cost)

    def degree_in_out(self, x:int):
        return self._graph.get_in_degree(x), self._graph.get_out_degree(x)

    def in_edges(self, x:int):
        """Returns an iterator over sources of inbound edges to x."""
        return self._graph.in_edges(x)

    def out_edges(self, x:int):
        """Returns an iterator over targets of outbound edges from x."""
        return self._graph.out_edges(x)

    def add_edge(self, x:int, y:int, cost:int):
        self._graph.add_edge(x,y,cost)

    def remove_edge(self, x:int, y:int):
        self._graph.remove_edge(x,y)

    def add_vertex(self, x:int):
        self._graph.add_vertex(x)

    def remove_vertex(self, x:int):
        self._graph.remove_vertex(x)

    def copy_graph(self):
        new_service = GraphService()
        new_service._graph = self._graph.copy()
        return new_service


    # !!!ADDED FOR PRACTICAL WORK NUMBER 2!!!

    def make_undirected(self) -> Graph:
        """
        Returns a copy of the graph where every directed edge (x,y)
        also has the reverse (y,x), making it undirected.
        The original graph is not modified.
        """
        undirected = self._graph.copy()
        for x, y in self._graph.get_edges():
            if not undirected.is_edge(y, x):
                undirected.add_edge(y, x, undirected.get_cost_of_edge(x, y))
        return undirected

    def dfs_component(self, graph: Graph, start: int, visited: set) -> set:
        """
        Iterative DFS from 'start' vertex on an undirected graph.

        Marks all reached vertices in 'visited' set and returns the
        set of vertices belonging to this component.
        """

        component_vertices = set()
        stack = [start]

        while stack:
            v = stack.pop()
            if v in visited:
                continue

            visited.add(v)
            component_vertices.add(v)

            for neighbour in graph.out_edges(v):
                if neighbour not in visited:
                    stack.append(neighbour)

        return component_vertices

    def build_component_graph(self, component_vertices: set) -> Graph:
        """
        Builds a Graph object from a set of vertices, keeping only
        the edges between them from the original (directed) graph.
        """

        comp_graph = Graph()

        for v in component_vertices:
            comp_graph.add_vertex(v)

        for v in component_vertices:
            for w in self._graph.out_edges(v):
                if w in component_vertices:
                    comp_graph.add_edge(v, w, self._graph.get_cost_of_edge(v, w))

        return comp_graph

    def connected_components(self) -> list[Graph]:
        """
        Finds all connected components of the graph.
        Converts to undirected first, then runs DFS from each unvisited vertex.
        Returns a list of Graph objects.
        Complexity: O(V + E)
        """

        undirected = self.make_undirected()

        visited = set()
        components = []

        for start in undirected.vertices():
            if start not in visited:
                component_vertices = self.dfs_component(undirected, start, visited)
                components.append(self.build_component_graph(component_vertices))

        return components


    # ADDED FOR PRACTICAL WORK NUMBER 3

    def build_cost_matrix(self):
        """
        Builds the initial cost matrix for the graph.
        W[i][i] = 0
        W[i][j] = cost(i,j)  if edge exists
        W[i][j] = INF         otherwise
        """

        n = self.no_of_vertices()
        W = [[float('inf')] * n for _ in range(n)]

        for i in range(n):
            W[i][i] = 0

        for i in self.get_vertices():
            for j in self.out_edges(i):
                W[i][j] = self._graph.get_cost_of_edge(i, j)

        return W

    def extend_matrix(self, D, W):
        """
        Compute the next power of matrix D
        :param D: the matrix of the shortest paths of length m
        :param W: the initial cost matrix
        """

        n = self.no_of_vertices()
        newD = [[float('inf')] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                for k in range(n):  # for every pair of vertices i and j, check for very possible vertex k
                    if D[i][k] != float('inf') and W[k][j] != float('inf'):     #check if paths exist so far
                        cost = D[i][k] + W[k][j]
                        if cost < newD[i][j]:
                            newD[i][j] = cost

        return newD


    def matrix_multiplication(self,start, end):
        if start not in self.get_vertices():
            raise ValueError("Invalid starting vertex!")
        if end not in self.get_vertices():
            raise ValueError("Invalid ending vertex!")

        n = self.no_of_vertices()
        W = self.build_cost_matrix()
        currentD = W

        #used for printing in the UI
        intermediate_matrices = [("D^1 (initial)", [row[:] for row in W])]


        for m in range(2,n):  #with every iteration, construct the paths with 1 more edge
            currentD = self.extend_matrix(currentD, W)
            intermediate_matrices.append((f"D^{m}", [row[:] for row in currentD]))

        lastD = currentD
        extraD = self.extend_matrix(lastD, W)   #compute one more matrix for negative cost cycle check
        for i in range(n):
            for j in range(n):
                if extraD[i][j] < lastD[i][j]:
                    raise ValueError("Negative cost cycle detected in the graph.")
        cost = lastD[start][end]
        if cost == float('inf'):
            raise ValueError(f"No walk exists from {start} to {end}.")


        #reconstruct the actual path
        path = [start]
        current = start
        while current!=end:
            for neighbour in self.out_edges(current):
                road_cost = self._graph.get_cost_of_edge(current, neighbour)
                remaining_cost = lastD[neighbour][end]

                if road_cost + remaining_cost == lastD[current][end]:
                    path.append(neighbour)
                    current = neighbour
                    break

        return cost, path, intermediate_matrices



    # ADDED FOR PRACTICAL WORK NUMBER 4
    # we already have the undirected graph, in a previous method

    def prim_algorithm(self, start_node: int):
        """
        Constructs the Minimum Spanning Tree starting from start_node.
        Uses make_undirected() to handle directed input as undirected.
        """
        if not self._graph.has_vertex(start_node):
            raise ValueError(f"Vertex {start_node} does not exist!")

        #make the graph undirected
        undirected_graph = self.make_undirected()

        vertices = list(undirected_graph.vertices())
        n = len(vertices)


        visited = {v:False for v in vertices}
        parent = {v:-1 for v in vertices}
        distance = {v: float('inf') for v in vertices}

        distance[start_node] = 0
        mst_edges = []
        total_cost = 0

        for _ in range(n):
            # find the unvisited vertex, with minimum cost
            min_val = float('inf')
            p = -1

            for v in vertices:
                if not visited[v] and distance[v] < min_val:
                    min_val = distance[v]
                    p = v

            #if no node is found, then the graph is not connected!
            if p == -1:
                break

            visited[p] = True

            #if it's not the root, add it to the result
            if parent[p] != -1:
                mst_edges.append((parent[p], p, min_val))
                total_cost += min_val

            #update the "parent"
            for neighbour in undirected_graph.out_edges(p):
                cost = undirected_graph.get_cost_of_edge(p, neighbour)
                if not visited[neighbour] and cost < distance[neighbour]:
                    distance[neighbour] = cost
                    parent[neighbour] = p


        return mst_edges, total_cost


    #ADDED FOR PRACTICAL WORK NUMBER 5
    def bron_kerbosch_recursive(self, graph: Graph, R: set, P: set, X: set, global_max: list) -> None:
        """
        Recursive implementation of the Bron-Kerbosch algorithm.
        Updates global_max[0] whenever a larger maximal clique is identified.

        R: the current growing clique
        P: candidate vertices that are connected to all vertices currently in R
        X: vertices that have already been processed in earlier branches and are mutually connected
        to everything in R; they are used to prevent finding duplicate cliques
        """
        #if P and X are both empty, then R is the maximal clique
        if not P and not X:
            if len(R) > len(global_max[0]):
                global_max[0] = list(R)
            return

        #for each vertex v in P
        for v in list(P):
            #take the neighbours of each vertex
            neighbors_v = set(graph.out_edges(v))

            self.bron_kerbosch_recursive(
                graph,
                R.union({v}),
                P.intersection(neighbors_v),
                X.intersection(neighbors_v),
                global_max)

            P.remove(v)
            X.add(v)

    def find_maximum_clique(self) -> list[int]:
        """
        Converts the graph structure to an undirected view, initializes sets,
        and starts the recursive Bron-Kerbosch algorithm.
        """
        undirected_graph = self.make_undirected()

        #initial call sets: R = empty, X = empty, P = all graph vertices
        R_set = set()
        P_set = set(undirected_graph.vertices())
        X_set = set()

        #track state across recursion levels
        global_max_holder = [[]]

        self.bron_kerbosch_recursive(undirected_graph, R_set, P_set, X_set, global_max_holder)

        return sorted(global_max_holder[0])