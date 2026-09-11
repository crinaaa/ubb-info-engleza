from service import GraphService


class ConsoleUI:
    def __init__(self):
        self._service = GraphService()
        self._copies: dict[str, GraphService] = {}
        self._components: list = []

    def print_menu(self):

        print("1. Print the number of vertices.")  #done
        print("2. Parse the set of vertices.")  #done
        print("3. Check if there is an edge between 2 given vertices.")     #done
        print("4. Get the in and out degree of a given vertex.")    #done
        print("5. Parse the outbound edges.")       #done
        print("6. Parse the inbound edges.")        #done
        print("7. Print the cost of a given edge.")     #done
        print("8. Modify the cost of a given edge.")    #done
        print("9. Add an edge.")
        print("10. Remove an edge.")
        print("11. Add a vertex.")
        print("12. Remove a vertex.")
        print("13. Copy the graph.")
        print("14. Read the graph from a file.")    #done
        print("15. Write the graph to a file.")     #done
        print("16. Generate random graph.")
        print("17. Switch to a copy of the graph.")
        print("18. Find the connected components of a graph using DFS.")
        print("19. Matrix multiplication algorithm")
        print("20. Find Minimum Spanning Tree (Prim's Algorithm)")
        print("21. Find the clique of maximum size.")


    def read_graph_ui(self):
        filename = input("Filename to read from: ").strip()
        try:
            self._service.read_graph(filename)
            print(f"Graph loaded: {self._service.no_of_vertices()} vertices, "
                  f"{self._service.no_of_edges()} edges.")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except PermissionError as e:
            print(f"Error: {e}")

    def write_graph_ui(self):
        filename = input("Filename to write to: ").strip()
        try:
            self._service.write_graph(filename)
            print(f"Graph written to '{filename}'.")
        except PermissionError as e:
            print(f"Error: {e}")


    def number_of_vertices_ui(self):
        print(self._service.no_of_vertices(),"\n")

    def parse_vertices_ui(self):
        vertices = sorted(self._service.get_vertices())
        if not vertices:
            print("There are no vertices in the graph.")
        else:
            print(vertices)

    def check_edge_ui(self):
        x = int(input("Enter the first vertex: "))
        y = int(input("Enter the second vertex: "))
        if self._service.check_edge(x,y):
            cost = self._service.cost_of_edge(x,y)
            print(f"Yes, there is an edge between vertex {x} and vertex {y} with a cost of {cost}\n")
        else:
            print(f"No, there is not any edge between vertex {x} and vertex {y}\n")

    def get_in_out_degree_ui(self):
        v = int(input("Enter vertex: "))
        try:
            v_in, v_out = self._service.degree_in_out(v)
            print(f"In-degree:  {v_in}")
            in_sources = list(self._service.in_edges(v))
            print(f"  Sources of inbound edges:  {in_sources}")
            print(f"Out-degree: {v_out}")
            out_targets = list(self._service.out_edges(v))
            print(f"  Targets of outbound edges: {out_targets}")
        except ValueError as e:
            print(f"Error: {e}")

    def parse_in_edges(self):
        v = int(input("Enter vertex: "))
        try:
            sources = list(self._service.in_edges(v))
            if not sources:
                print(f"Vertex {v} has no inbound edges.")
            else:
                for x in sources:
                    cost = self._service.cost_of_edge(x, v)
                    print(f"  {x} → {v}  (cost: {cost})")
        except ValueError as e:
            print(f"Error: {e}")

    def parse_out_edges(self):
        v = int(input("Enter vertex: "))
        try:
            targets = list(self._service.out_edges(v))
            if not targets:
                print(f"Vertex {v} has no outbound edges.")
            else:
                for y in targets:
                    cost = self._service.cost_of_edge(v, y)
                    print(f"  {v} → {y}  (cost: {cost})")
        except ValueError as e:
            print(f"Error: {e}")

    def get_edge_cost_ui(self):
        x = int(input("Enter source vertex: "))
        y = int(input("Enter target vertex: "))
        try:
            print(f"Cost of ({x} → {y}): {self._service.cost_of_edge(x, y)}")
        except ValueError as e:
            print(f"Error: {e}")

    def modify_edge_cost_ui(self):
        x = int(input("Enter source vertex: "))
        y = int(input("Enter target vertex: "))
        value = int(input("Enter the new cost: "))
        try:
            self._service.set_new_cost(x, y, value)
            print("Cost updated successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def add_edge_ui(self):
        x = int(input("Enter source vertex: "))
        y = int(input("Enter target vertex: "))
        cost = int(input("Enter cost: "))
        try:
            self._service.add_edge(x, y, cost)
            print(f"Edge ({x} → {y}) added with cost {cost}.")
        except ValueError as e:
            print(f"Error: {e}")

    def remove_edge_ui(self):
        x = int(input("Enter source vertex: "))
        y = int(input("Enter target vertex: "))
        try:
            self._service.remove_edge(x, y)
            print(f"Edge ({x} → {y}) removed.")
        except ValueError as e:
            print(f"Error: {e}")

    def add_vertex_ui(self):
        v = int(input("Enter vertex id to add: "))
        try:
            self._service.add_vertex(v)
            print(f"Vertex {v} added.")
        except ValueError as e:
            print(f"Error: {e}")

    def remove_vertex_ui(self):
        v = int(input("Enter vertex id to remove: "))
        try:
            self._service.remove_vertex(v)
            print(f"Vertex {v} and all its incident edges removed.")
        except ValueError as e:
            print(f"Error: {e}")

    def deep_copy_ui(self):
        name = input("Give this copy a name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        self._copies[name] = self._service.copy_graph()
        print(f"Graph copied as '{name}'.")
        if self._copies:
            print(f"Available copies: {list(self._copies.keys())}")

    def switch_to_copy_ui(self):
        if not self._copies:
            print("No copies available.")
            return
        print(f"Available copies: {list(self._copies.keys())}")
        name = input("Enter copy name to switch to: ").strip()
        if name not in self._copies:
            print(f"No copy named '{name}'.")
            return
        self._service = self._copies[name]
        print(f"Switched to copy '{name}'. "
              f"({self._service.no_of_vertices()} vertices, "
              f"{self._service.no_of_edges()} edges)")

    def generate_random_graph_ui(self):
        try:
            n = int(input("Number of vertices: "))
            m = int(input("Number of edges: "))
            self._service.generate_random(n, m)
            print(f"Random graph generated: {n} vertices, {m} edges.")
        except ValueError as e:
            print(f"Error: {e}")


    #!!!ADDED FOR PRACTICAL WORK NUMBER 2!!!

    def connected_components_ui(self):
        components = self._service.connected_components()
        self._components = components

        if not components:
            print("The graph is empty. No components found.")
            return

        print(f"\nFound {len(components)} connected component(s):")


        # iterate through each component, to show vertices and edges
        for idx, comp in enumerate(components, start=1):
            vertices = sorted(comp.vertices())
            edges = list(comp.get_edges())

            print(f"Component {idx}:")
            print(f"  Vertices ({comp.nr_vertices()}): {vertices}")

            # if edges:
            #     edge_list = [f"{x}→{y}({comp.get_cost_of_edge(x, y)})" for x, y in edges]
            #     print(f"  Edges    ({comp.nr_edges()}): {', '.join(edge_list)}")
            # else:
            #     print(f"  Edges    : (none)")
        print()


    # ADDED FOR PRACTICAL WORK NUMBER 3

    def _format_matrix(self, matrix, n):
        col_w = 8
        header = " " * 5 + "".join(f"{v:>{col_w}}" for v in range(n))
        lines = [header, " " * 5 + "-" * (col_w * n)]
        for i, row in enumerate(matrix):
            cells = ["INF" if v == float('inf') else str(v) for v in row]
            lines.append(f"{i:>4} |" + "".join(f"{c:>{col_w}}" for c in cells))
        return "\n".join(lines)

    def lowest_cost_ui(self):
        try:
            start = int(input("Enter source vertex: "))
            end = int(input("Enter target vertex: "))

            cost, path, matrices = self._service.matrix_multiplication(start, end)

            n = self._service.no_of_vertices()
            print("\n--- Intermediate matrices ---")
            for label, matrix in matrices:
                print(f"\n  {label}:")
                print(self._format_matrix(matrix, n))

            print(f"\nLowest cost walk from {start} to {end}: {' -> '.join(map(str, path))}")
            print(f"Total cost: {cost}\n")

        except ValueError as e:
            print(f"Error: {e}")


    #ADDED FOR PRACTICAL WORK NUMBER 4
    def prim_mst_ui(self):
        try:
            start_node = int(input("Enter the starting vertex for Prim's algorithm: "))
            mst, total_cost = self._service.prim_algorithm(start_node)

            if len(mst) < self._service.no_of_vertices() - 1:
                print("\nThe graph is not connected. This is the MST for the starting component.")

            print("\nMinimum Spanning Tree edges (u - v : cost):")
            for u, v, cost in mst:
                print(f"  {u} - {v} : {cost}")
            print(f"Total MST Cost: {total_cost}\n")
        except ValueError as e:
            print(f"Error: {e}")


    #ADDED FOR PRACTICAL WORK NUMBER 5
    def maximum_clique_ui(self):
        try:
            clique = self._service.find_maximum_clique()
            if not clique:
                print("\nThe graph contains no vertices. No clique exists.")
            else:
                print(f"\nMaximum Clique found: {clique}")
                print(f"Size of the Maximum Clique: {len(clique)}\n")
        except Exception as e:
            print(f"Error while processing clique: {e}")


    def run(self):
        while True:
            self.print_menu()
            try:
                command = int(input("> "))
                if command == 1:
                    self.number_of_vertices_ui()
                elif command == 2:
                    self.parse_vertices_ui()
                elif command == 3:
                    self.check_edge_ui()
                elif command == 4:
                    self.get_in_out_degree_ui()
                elif command == 5:
                    self.parse_out_edges()
                elif command == 6:
                    self.parse_in_edges()
                elif command == 7:
                    self.get_edge_cost_ui()
                elif command == 8:
                    self.modify_edge_cost_ui()
                elif command == 9:
                    self.add_edge_ui()
                elif command == 10:
                    self.remove_edge_ui()
                elif command == 11:
                    self.add_vertex_ui()
                elif command == 12:
                    self.remove_vertex_ui()
                elif command == 13:
                    self.deep_copy_ui()
                elif command == 14:
                    self.read_graph_ui()
                elif command == 15:
                    self.write_graph_ui()
                elif command == 16:
                    self.generate_random_graph_ui()
                elif command == 17:
                    self.switch_to_copy_ui()
                elif command == 18:
                    self.connected_components_ui()
                elif command == 19:
                    self.lowest_cost_ui()
                elif command == 20:
                    self.prim_mst_ui()
                elif command == 21:
                    self.maximum_clique_ui()
                elif command == 0:
                    print("Exiting!")
                    break
                else:
                    print("Invalid command!")
            except ValueError:
                print("Invalid input! Try again!")