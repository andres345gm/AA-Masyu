def read_input_file(filename):
    with open(filename, 'r') as file:
        n = int(file.readline())
        pearls = []
        for line in file:
            line_aux = line.strip()
            pearl = line_aux.split(',')
            pearl = [int(i) for i in pearl]
            pearls.append(pearl)
        # End for
        return n, pearls
    # End with


# End def


class Board:
    def __init__(self, n, pearls_list):
        self.n = n
        self.pearls_list = pearls_list
        self.matrix = [[0 for _ in range(n)] for _ in range(n)]
        self.pearls = [[0 for _ in range(n)] for _ in range(n)]
        for pearl in pearls_list:
            self.pearls[pearl[0] - 1][pearl[1] - 1] = pearl[2]
        # End for

    # End def

    def find_start_point(self):
        i = self.pearls_list[0][0] - 1
        j = self.pearls_list[0][1] - 1
        node = (i, j)
        return node

    def verify_board(self):
        return self.verify_board_aux(self.matrix)

    def verify_board_aux(self, matrix):
        if not self.verify_pearls(matrix):
            return False
        # End if
        graph = self.board_to_graph(matrix)
        if self.verify_cycle(graph)[0]:
            if self.verify_pearls_in_cycle(self.verify_cycle(graph)[1]):
                return True
        # End if
        return False

    # End def

    def verify_pearls(self, matrix):
        for pearl in self.pearls_list:
            row, col = pearl[0] - 1, pearl[1] - 1
            if pearl[2] == 1:
                if not self.verify_white_pearl(matrix, row, col):
                    return False
                # End if
            elif pearl[2] == 2:
                if not self.verify_black_pearl(matrix, row, col):
                    return False
                # End if
            # End if
        # End for

        return True

    # End def

    def verify_white_pearl(self, matrix, row, col):
        # Verification if the line is horizontal
        if col - 1 >= 0 and col + 1 < self.n:
            if matrix[row][col] == 1:
                left_turn = matrix[row][col - 1] == 3 or matrix[row][col - 1] == 4
                right_turn = matrix[row][col + 1] == 5 or matrix[row][col + 1] == 6
                return left_turn or right_turn
            # End if
        if row - 1 >= 0 and row + 1 < self.n:
            # Verification if the line is vertical
            if matrix[row][col] == 2:
                top_turn = matrix[row - 1][col] == 4 or matrix[row - 1][col] == 5
                bottom_turn = matrix[row + 1][col] == 3 or matrix[row + 1][col] == 6
                return top_turn or bottom_turn
            # End if
        return False

    # end def

    def get_neighbours(self, matrix, row, col):
        left, right, up, down = False, False, False, False
        if row - 1 >= 0:
            up = matrix[row - 1][col] == 2
        if row + 1 < self.n:
            down = matrix[row + 1][col] == 2
        if col - 1 >= 0:
            left = matrix[row][col - 1] == 1
        if col + 1 < self.n:
            right = matrix[row][col + 1] == 1
        return up, down, left, right

    def get_connections(self, matrix, i, j):
        left_c, right_c, up_c, down_c = False, False, False, False
        if i - 1 >= 0:
            up_c = matrix[i - 1][j] == 2 or matrix[i - 1][j] == 4 or matrix[i - 1][j] == 5
        if i + 1 < self.n:
            down_c = matrix[i + 1][j] == 2 or matrix[i + 1][j] == 3 or matrix[i + 1][j] == 6
        if j - 1 >= 0:
            left_c = matrix[i][j - 1] == 1 or matrix[i][j - 1] == 3 or matrix[i][j - 1] == 4
        if j + 1 < self.n:
            right_c = matrix[i][j + 1] == 1 or matrix[i][j + 1] == 5 or matrix[i][j + 1] == 6
        return left_c, right_c, up_c, down_c

    def verify_black_pearl(self, matrix, row, col):
        up, down, left, right = self.get_neighbours(matrix, row, col)
        if matrix[row][col] == 3:
            return up and right
        elif matrix[row][col] == 4:
            return right and down
        elif matrix[row][col] == 5:
            return down and left
        elif matrix[row][col] == 6:
            return left and up
        return False

    def board_to_graph(self, matrix):
        graph = {}
        for i in range(self.n):
            for j in range(self.n):
                graph[(i, j)] = []
                left_c, right_c, up_c, down_c = self.get_connections(matrix, i, j)
                if matrix[i][j] == 1:
                    if left_c:
                        graph[(i, j)].append((i, j - 1))
                    if right_c:
                        graph[(i, j)].append((i, j + 1))
                elif matrix[i][j] == 2:
                    if up_c:
                        graph[(i, j)].append((i - 1, j))
                    if down_c:
                        graph[(i, j)].append((i + 1, j))
                elif matrix[i][j] == 3:
                    if up_c:
                        graph[(i, j)].append((i - 1, j))
                    if right_c:
                        graph[(i, j)].append((i, j + 1))
                elif matrix[i][j] == 4:
                    if right_c:
                        graph[(i, j)].append((i, j + 1))
                    if down_c:
                        graph[(i, j)].append((i + 1, j))
                elif matrix[i][j] == 5:
                    if down_c:
                        graph[(i, j)].append((i + 1, j))
                    if left_c:
                        graph[(i, j)].append((i, j - 1))
                elif matrix[i][j] == 6:
                    if left_c:
                        graph[(i, j)].append((i, j - 1))
                    if up_c:
                        graph[(i, j)].append((i - 1, j))
        return graph

    def verify_cycle(self, graph):
        visited = set()
        stack = []
        start_node = self.find_start_point()
        stack.append((start_node, None))  # Usamos una tupla para rastrear el nodo y su padre
        cycle_nodes = []  # Lista para almacenar los nodos del ciclo, si se encuentra
        parent = {}  # Diccionario para rastrear los predecesores de los nodos

        while stack:
            node, prev_node = stack.pop()
            visited.add(node)
            neighbours = graph[node]
            for neighbour in neighbours:
                if neighbour not in visited:
                    stack.append((neighbour, node))  # Agregamos el nodo y su padre a la pila
                    parent[neighbour] = node  # Actualizamos el predecesor del vecino
                elif neighbour != prev_node:  # Verificamos que el vecino no sea el padre del nodo actual
                    # Si encontramos un ciclo, agregamos los nodos del ciclo a la lista
                    cycle_nodes.append(neighbour)
                    current = node
                    while current != neighbour:
                        cycle_nodes.append(current)
                        current = parent[current]
                    cycle_nodes.append(neighbour)  # Agregamos el nodo vecino para completar el ciclo
                    return True, cycle_nodes  # Devolvemos True y la lista de nodos del ciclo
        return False, []  # Si no encontramos ciclos, devolvemos False y una lista vacía

    def verify_pearls_in_cycle(self, cycle):
        for pearl in self.pearls_list:
            row, col = pearl[0] - 1, pearl[1] - 1
            if (row, col) not in cycle:
                return False
            # End if
        # End for
        return True

    def solve_board(self):
        matrix = self.matrix.copy()
        marked_nodes = set()
        return self.solve_board_aux(matrix, marked_nodes)

    def solve_board_aux(self, matrix, marked_nodes):

        variables = self.find_variables(matrix, marked_nodes)
        if len(variables) == 0:
            if self.verify_board_aux(matrix):
                return matrix
            else:
                return None

        if self.verify_board_aux(matrix):
            return matrix

        domains = self.find_domains(matrix, marked_nodes)
        self.print_domain(domains)
        variable = self.select_variable(domains)
        # print("Variable", variable)
        for value in domains[variable]:
            print("Value", value)
            marked_nodes.add(variable)
            matrix[variable[0]][variable[1]] = value

            domains = self.find_domains(matrix, marked_nodes)
            if self.verify_domain(domains):
                result = self.solve_board_aux(matrix, marked_nodes)
                if result is not None:
                    return result
            marked_nodes.remove(variable)
            matrix[variable[0]][variable[1]] = 0
        return None

    """
    def solve_board(self, matrix):
        variables = self.find_variables(matrix)
        if len(variables) == 0:
            if self.verify_board_aux(matrix):
                return matrix
            else:
                return None
        if self.verify_board_aux(matrix):
            return matrix
        variable = variables[0]
        #domains = self.find_domains(matrix)
        for value in range(1, 7):
            matrix[variable[0]][variable[1]] = value
            result = self.solve_board(matrix)
            if result is not None:
                return result
            matrix[variable[0]][variable[1]] = 0
        return None
    """

    """
        def find_variables(self, matrix):
            variables = []
            for i in range(self.n):
                for j in range(self.n):
                    if matrix[i][j] == 0:
                        variables.append((i, j))
                    # End if
                # End for
            # End for
            return variables
    """

    def find_variables(self, matrix, marked_nodes):
        variables = []
        for i in range(self.n):
            for j in range(self.n):
                if (i, j) not in marked_nodes:
                    variables.append((i, j))
                # End if
            # End for
        # End for
        return variables


    def find_domains(self, matrix, marked_nodes):
        domain = {}
        for i in range(self.n):
            for j in range(self.n):
                if (i, j) not in marked_nodes:
                    domain[(i, j)] = []
                    left_c, right_c, up_c, down_c = self.get_connections(matrix, i, j)
                    if self.pearls[i][j] == 0:
                        domain[(i, j)] = self.empty_space_domain(matrix, i, j)
                    if self.pearls[i][j] == 1:
                        domain[(i, j)] = self.white_pearl_domain(matrix, i, j)
                    elif self.pearls[i][j] == 2:
                        domain[(i, j)] = self.black_pearl_domain(matrix, i, j)

                    self.reduce_domain_in_edges(matrix, domain, i, j)
                # End if
            # End for
        # End for
        return domain

    def empty_space_domain(self, matrix, row, col):
        left_c, right_c, up_c, down_c = self.get_connections(matrix, row, col)
        domain = []
        domain.append(0)
        if left_c and right_c:
            domain.append(1)
        elif up_c and down_c:
            domain.append(2)
        elif up_c and right_c:
            domain.append(3)
        elif right_c and down_c:
            domain.append(4)
        elif down_c and left_c:
            domain.append(5)
        elif left_c and up_c:
            domain.append(6)
        elif left_c:
            domain.append(1)
            domain.append(5)
            domain.append(6)
        elif right_c:
            domain.append(1)
            domain.append(3)
            domain.append(4)
        elif up_c:
            domain.append(2)
            domain.append(3)
            domain.append(6)
        elif down_c:
            domain.append(2)
            domain.append(5)
            domain.append(4)
        else:
            domain.append(1)
            domain.append(2)
            domain.append(3)
            domain.append(4)
            domain.append(5)
            domain.append(6)
        """
        # Revisar que no este al lado de una perla negra
        adjacent = self.get_adjacent(matrix, row, col)
        for adj in adjacent:
            if self.pearls[adj[0]][adj[1]] == 2:
                if matrix[adj[0]][adj[1]] == 3:
                    pass
                if matrix[adj[0]][adj[1]] == 4:
                    pass
                if matrix[adj[0]][adj[1]] == 5:
                    pass
                if matrix[adj[0]][adj[1]] == 6:
                    pass
        """
        return domain

    def white_pearl_domain(self, matrix, row, col):
        left_c, right_c, up_c, down_c = self.get_connections(matrix, row, col)
        domain = []
        if left_c and right_c:
            if self.verify_white_pearl_horizontal(matrix, row, col):
                domain.append(1)
        elif up_c and down_c:
            if self.verify_white_pearl_vertical(matrix, row, col):
                domain.append(2)
        elif left_c or right_c:
            domain.append(1)
        elif up_c or down_c:
            domain.append(2)
        else:
            domain.append(1)
            domain.append(2)
        return domain

    def black_pearl_domain(self, matrix, row, col):
        domain = []
        s_up, s_down, s_left, s_right = self.get_neighbours(matrix, i, j)
        if s_up and s_right:
            domain.append(3)
        if s_right and s_down:
            domain.append(4)
        if s_down and s_left:
            domain.append(5)
        if s_left and s_up:
            domain.append(6)
        if s_up:
            domain.append(3)
            domain.append(6)
        if s_right:
            domain.append(3)
            domain.append(4)
        if s_down:
            domain.append(4)
            domain.append(5)
        if s_left:
            domain.append(5)
            domain.append(6)
        else:
            domain.append(3)
            domain.append(4)
            domain.append(5)
            domain.append(6)
        return domain

    def reduce_domain_in_edges(self, matrix, domain, i, j):
        if i == 0:
            if 2 in domain[(i, j)]:
                domain[(i, j)].remove(2)
            if 3 in domain[(i, j)]:
                domain[(i, j)].remove(3)
            if 6 in domain[(i, j)]:
                domain[(i, j)].remove(6)

        if j == 0:
            if 1 in domain[(i, j)]:
                domain[(i, j)].remove(1)
            if 5 in domain[(i, j)]:
                domain[(i, j)].remove(5)
            if 6 in domain[(i, j)]:
                domain[(i, j)].remove(6)

        if i == self.n - 1:
            if 2 in domain[(i, j)]:
                domain[(i, j)].remove(2)
            if 5 in domain[(i, j)]:
                domain[(i, j)].remove(5)
            if 4 in domain[(i, j)]:
                domain[(i, j)].remove(4)

        if j == self.n - 1:
            if 1 in domain[(i, j)]:
                domain[(i, j)].remove(1)
            if 3 in domain[(i, j)]:
                domain[(i, j)].remove(3)
            if 4 in domain[(i, j)]:
                domain[(i, j)].remove(4)

    def get_adjacent(self, matrix, row, col):
        adjacent = []
        if row - 1 >= 0:
            adjacent.append((row - 1, col))
        if row + 1 < self.n:
            adjacent.append((row + 1, col))
        if col - 1 >= 0:
            adjacent.append((row, col - 1))
        if col + 1 < self.n:
            adjacent.append((row, col + 1))
        return adjacent


    """
    def find_domains(self, matrix):
        domain = {}
        for i in range(self.n):
            for j in range(self.n):
                if matrix[i][j] == 0:
                    domain[(i, j)] = []
                    left_c, right_c, up_c, down_c = self.get_connections(matrix, i, j)

                    if self.pearls[i][j] == 0:
                        domain[(i, j)].append(0)
                        if left_c and right_c:
                            domain[(i, j)].append(1)
                        elif up_c and down_c:
                            domain[(i, j)].append(2)
                        elif up_c and right_c:
                            domain[(i, j)].append(3)
                        elif right_c and down_c:
                            domain[(i, j)].append(4)
                        elif down_c and left_c:
                            domain[(i, j)].append(5)
                        elif left_c and up_c:
                            domain[(i, j)].append(6)
                        elif left_c:
                            domain[(i, j)].append(1)
                            domain[(i, j)].append(5)
                            domain[(i, j)].append(6)
                        elif right_c:
                            domain[(i, j)].append(1)
                            domain[(i, j)].append(3)
                            domain[(i, j)].append(4)
                        elif up_c:
                            domain[(i, j)].append(2)
                            domain[(i, j)].append(3)
                            domain[(i, j)].append(6)
                        elif down_c:
                            domain[(i, j)].append(2)
                            domain[(i, j)].append(5)
                            domain[(i, j)].append(4)
                        else:
                            domain[(i, j)].append(1)
                            domain[(i, j)].append(2)
                            domain[(i, j)].append(3)
                            domain[(i, j)].append(4)
                            domain[(i, j)].append(5)
                            domain[(i, j)].append(6)
                    if self.pearls[i][j] == 1:
                        if left_c and right_c:
                            if self.verify_white_pearl_horizontal(matrix, i, j):
                                domain[(i, j)].append(1)
                        elif up_c and down_c:
                            if self.verify_white_pearl_vertical(matrix, i, j):
                                domain[(i, j)].append(2)
                        elif left_c or right_c:
                            domain[(i, j)].append(1)
                        elif up_c or down_c:
                            domain[(i, j)].append(2)
                        else:
                            domain[(i, j)].append(1)
                            domain[(i, j)].append(2)
                    elif self.pearls[i][j] == 2:
                        s_up, s_down, s_left, s_right = self.get_neighbours(matrix, i, j)
                        if s_up and s_right:
                            domain[(i, j)].append(3)
                        if s_right and s_down:
                            domain[(i, j)].append(4)
                        if s_down and s_left:
                            domain[(i, j)].append(5)
                        if s_left and s_up:
                            domain[(i, j)].append(6)
                        if s_up:
                            domain[(i, j)].append(3)
                            domain[(i, j)].append(6)
                        if s_right:
                            domain[(i, j)].append(3)
                            domain[(i, j)].append(4)
                        if s_down:
                            domain[(i, j)].append(4)
                            domain[(i, j)].append(5)
                        if s_left:
                            domain[(i, j)].append(5)
                            domain[(i, j)].append(6)
                        else:
                            domain[(i, j)].append(3)
                            domain[(i, j)].append(4)
                            domain[(i, j)].append(5)
                            domain[(i, j)].append(6)

                    if i == 0:
                        if 2 in domain[(i, j)]:
                            domain[(i, j)].remove(2)
                        if 3 in domain[(i, j)]:
                            domain[(i, j)].remove(3)
                        if 6 in domain[(i, j)]:
                            domain[(i, j)].remove(6)

                    if j == 0:
                        if 1 in domain[(i, j)]:
                            domain[(i, j)].remove(1)
                        if 5 in domain[(i, j)]:
                            domain[(i, j)].remove(5)
                        if 6 in domain[(i, j)]:
                            domain[(i, j)].remove(6)

                    if i == self.n - 1:
                        if 2 in domain[(i, j)]:
                            domain[(i, j)].remove(2)
                        if 5 in domain[(i, j)]:
                            domain[(i, j)].remove(5)
                        if 4 in domain[(i, j)]:
                            domain[(i, j)].remove(4)

                    if j == self.n - 1:
                        if 1 in domain[(i, j)]:
                            domain[(i, j)].remove(1)
                        if 3 in domain[(i, j)]:
                            domain[(i, j)].remove(3)
                        if 4 in domain[(i, j)]:
                            domain[(i, j)].remove(4)

                # End if
            # End for
        # End for
        return domain
        
    """

    """
    def find_domains(self, matrix):
        domain = {}
        for i in range(self.n):
            for j in range(self.n):
                if matrix[i][j] == 0:
                    domain[(i, j)] = []
                    if self.pearls[i][j] == 0:
                        domain[(i, j)].append(1)
                        domain[(i, j)].append(2)
                        domain[(i, j)].append(3)
                        domain[(i, j)].append(4)
                        domain[(i, j)].append(5)
                        domain[(i, j)].append(6)
                    if self.pearls[i][j] == 1:
                        domain[(i, j)].append(1)
                        domain[(i, j)].append(2)
                    if self.pearls[i][j] == 2:
                        domain[(i, j)].append(3)
                        domain[(i, j)].append(4)
                        domain[(i, j)].append(5)
                        domain[(i, j)].append(6)
        return domain
    """

    def verify_domain(self, domains):
        for key in domains.keys():
            if len(domains[key]) == 0:
                return False
        return True

    def select_variable(self, domain):
        domain_copy = domain.copy()
        for key in domain.keys():
            if self.pearls[key[0]][key[1]] == 0:
                del domain_copy[key]

        used_domain = domain
        if len(domain_copy) > 0:
            used_domain = domain_copy
            print("New domain")
            self.print_domain(used_domain)
        min_domain = float('inf')
        variable = None
        for key in used_domain.keys():
            if len(used_domain[key]) < min_domain:
                min_domain = len(used_domain[key])
                variable = key
        print("Variable", variable)
        return variable

    def verify_white_pearl_horizontal(self, matrix, row, col):
        # Verification if the line is horizontal
        if col - 1 >= 0 and col + 1 < self.n:
            left_turn = matrix[row][col - 1] == 3 or matrix[row][col - 1] == 4
            right_turn = matrix[row][col + 1] == 5 or matrix[row][col + 1] == 6
            return left_turn or right_turn
            # End if
        return False

    # end def
    def verify_white_pearl_vertical(self, matrix, row, col):
        # Verification if the line is vertical
        if row - 1 >= 0 and row + 1 < self.n:
            top_turn = matrix[row - 1][col] == 4 or matrix[row - 1][col] == 5
            bottom_turn = matrix[row + 1][col] == 3 or matrix[row + 1][col] == 6
            return top_turn or bottom_turn
            # End if
        return False

    # End def

    def print_domain(self, domain):
        for key in domain.keys():
            print(key, "->", domain[key])

# End class
