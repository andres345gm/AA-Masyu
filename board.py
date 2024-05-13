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

    def get_straight_connections(self, matrix, row, col):
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
        up, down, left, right = self.get_straight_connections(matrix, row, col)
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

        domains = self.find_domains(matrix, variables)
        self.print_board(matrix)
        self.print_domain(domains)
        print("------")
        variable = self.select_variable(domains)
        variables.remove(variable)
        marked_nodes.add(variable)
        for value in domains[variable]:
            matrix[variable[0]][variable[1]] = value
            new_domains = self.find_domains(matrix, variables)
            #if self.verify_domain(new_domains):
            result = self.solve_board_aux(matrix, marked_nodes)
            if result is not None:
                return result
        marked_nodes.remove(variable)
        matrix[variable[0]][variable[1]] = 0
        return None


    def find_variables(self, matrix, marked_nodes):
        variables = set()
        if len(marked_nodes) < len(self.pearls_list):
            for pearl in self.pearls_list:
                row, col = pearl[0] - 1, pearl[1] - 1
                if (row, col) not in marked_nodes:
                    variables.add((row, col))
            return list(variables)
            #return variables
        for i in range(self.n):
            for j in range(self.n):
                if (i, j) not in marked_nodes:
                    left_c, right_c, up_c, down_c = self.get_connections(matrix, i, j)
                    if left_c or right_c or up_c or down_c:
                        variables.add((i, j))
                    #variables.add((i, j))
                # End if
            # End for
        return list(variables)


    def find_domains(self, matrix, variables):
        domain = {}
        for variable in variables:
            i, j = variable
            domain[(i, j)] = []
            left_c, right_c, up_c, down_c = self.get_connections(matrix, i, j)
            if self.pearls[i][j] == 0:
                domain[(i, j)] = self.empty_space_domain(matrix, i, j)
                # self.empty_space_special_cases_domain(matrix, domain, i, j)
                self.remove_domain_values_that_create_a_cross(matrix, domain, i, j)
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
        # domain.append(0)
        if left_c and right_c:
            domain = [1]
        elif up_c and down_c:
            domain = [2]
        elif up_c and right_c:
            domain = [3]
        elif right_c and down_c:
            domain = [4]
        elif down_c and left_c:
            domain = [5]
        elif left_c and up_c:
            domain = [6]
        elif left_c:
            domain = [1, 5, 6]
        elif right_c:
            domain = [1, 3, 4]
        elif up_c:
            domain = [2, 3, 6]
        elif down_c:
            domain = [2, 4, 5]
        else:
            domain = [1, 2, 3, 4, 5, 6]

        return domain

    def remove_domain_values_that_create_a_cross(self, matrix, domain, row, col):
        left_c, right_c, up_c, down_c = self.get_connections(matrix, row, col)
        left_v, right_v, up_v, down_v = self.get_adjacent_values(matrix, row, col)
        if left_c and (right_v == 2 or right_v == 3 or right_v == 4):
            if 1 in domain[(row, col)]:
                domain[(row, col)].remove(1)
        if right_c and (left_v == 2 or left_v == 5 or left_v == 6):
            if 1 in domain[(row, col)]:
                domain[(row, col)].remove(1)
        if up_c and (down_v == 1 or down_v == 4 or down_v == 5):
            if 2 in domain[(row, col)]:
                domain[(row, col)].remove(2)
        if down_c and (up_v == 1 or up_v == 3 or up_v == 6):
            if 2 in domain[(row, col)]:
                domain[(row, col)].remove(2)


    def get_adjacent_values(self, matrix, row, col):
        left_v, right_v, up_v, down_v = None, None, None, None
        if col - 1 >= 0:
            left_v = matrix[row][col - 1]
        if col + 1 < self.n:
            right_v = matrix[row][col + 1]
        if row - 1 >= 0:
            up_v = matrix[row - 1][col]
        if row + 1 < self.n:
            down_v = matrix[row + 1][col]
        return left_v, right_v, up_v, down_v


    def empty_space_special_cases_domain(self, matrix, domain, row, col):
        left_c, right_c, up_c, down_c = self.get_connections(matrix, row, col)
        left_wp, right_wp, up_wp, down_wp = self.get_adjacent_pearl(matrix, row, col, 1)
        left_bp, right_bp, up_bp, down_bp = self.get_adjacent_pearl(matrix, row, col, 2)
        if (left_c and left_bp) or (right_c and right_bp):
            domain[(row, col)] = [1]
        elif (up_c and up_bp) or (down_c and down_bp):
            domain[(row, col)] = [2]

        if left_c and left_wp:
            if col - 2 >= 0:
                if matrix[row][col - 2] == 1:
                    domain[(row, col)] = [5, 6]
        if right_c and right_wp:
            if col + 2 < self.n:
                if matrix[row][col + 2] == 1:
                    domain[(row, col)] = [3, 4]
        if up_c and up_wp:
            if row - 2 >= 0:
                if matrix[row - 2][col] == 2:
                    domain[(row, col)] = [3, 6]
        if down_c and down_wp:
            if row + 2 < self.n:
                if matrix[row + 2][col] == 2:
                    domain[(row, col)] = [4, 5]


    def get_adjacent_pearl(self, matrix, row, col, pearl_type):
        # Pearl type 1 -> White pearl
        # Pearl type 2 -> Black pearl
        left_p, right_p, up_p, down_p = False, False, False, False
        if row - 1 >= 0:
            up_p = self.pearls[row - 1][col] == pearl_type
        if row + 1 < self.n:
            down_p = self.pearls[row + 1][col] == pearl_type
        if col - 1 >= 0:
            left_p = self.pearls[row][col - 1] == pearl_type
        if col + 1 < self.n:
            right_p = self.pearls[row][col + 1] == pearl_type
        return up_p, down_p, left_p, right_p

    def white_pearl_domain(self, matrix, row, col):
        left_c, right_c, up_c, down_c = self.get_connections(matrix, row, col)
        domain = []
        if left_c and right_c:
            domain = [1]
        elif up_c and down_c:
            domain = [2]
        elif left_c or right_c:
            domain = [1]
        elif up_c or down_c:
            domain = [2]
        else:
            domain = [1, 2]
        return domain

    def black_pearl_domain(self, matrix, i, j):
        domain = []
        s_up, s_down, s_left, s_right = self.get_straight_connections(matrix, i, j)
        if s_up and s_right:
            domain = [3]
        elif s_right and s_down:
            domain = [4]
        elif s_down and s_left:
            domain = [5]
        elif s_left and s_up:
            domain = [6]
        elif s_up:
            domain = [3, 6]
        elif s_right:
            domain = [3, 4]
        elif s_down:
            domain = [4, 5]
        elif s_left:
            domain = [5, 6]
        else:
            domain = [3, 4, 5, 6]
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
        min_domain = float('inf')
        variable = None
        for key in used_domain.keys():
            if len(used_domain[key]) < min_domain:
                min_domain = len(used_domain[key])
                variable = key
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

    def print_board(self, matrix):
        print()
        for row in matrix:
            print(row)


# End class
