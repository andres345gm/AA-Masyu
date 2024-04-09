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
        if not self.verify_pearls():
            return False
        # End if
        graph = self.board_to_graph()
        if self.verify_cycle(graph):
            return True
        # End if
        return False
    # End def

    def verify_pearls(self):
        for pearl in self.pearls_list:
            row, col = pearl[0] - 1, pearl[1] - 1
            if pearl[2] == 1:
                if not self.verify_white_pearl(row, col):
                    return False
                # End if
            elif pearl[2] == 2:
                if not self.verify_black_pearl(row, col):
                    return False
                # End if
            # End if
        # End for

        return True

    # End def

    def verify_white_pearl(self, row, col):
        # Verification if the line is horizontal
        if col - 1 >= 0 and col + 1 < self.n:
            if self.matrix[row][col] == 1:
                left_turn = self.matrix[row][col - 1] == 3 or self.matrix[row][col - 1] == 4
                right_turn = self.matrix[row][col + 1] == 5 or self.matrix[row][col + 1] == 6
                return left_turn or right_turn
            # End if
        if row - 1 >= 0 and row + 1 < self.n:
            # Verification if the line is vertical
            if self.matrix[row][col] == 2:
                top_turn = self.matrix[row - 1][col] == 4 or self.matrix[row - 1][col] == 5
                bottom_turn = self.matrix[row + 1][col] == 3 or self.matrix[row + 1][col] == 6
                return top_turn or bottom_turn
            # End if
        return False

    # end def

    def verify_black_pearl(self, row, col):
        up, down, left, right = self.get_neighbours(row, col)
        if self.matrix[row][col] == 3:
            return up and right
        elif self.matrix[row][col] == 4:
            return right and down
        elif self.matrix[row][col] == 5:
            return down and left
        elif self.matrix[row][col] == 6:
            return left and up
        return False

    def get_neighbours(self, row, col):
        left, right, up, down = False, False, False, False
        if row - 1 >= 0:
            up = self.matrix[row - 1][col] == 2
        if row + 1 < self.n:
            down = self.matrix[row + 1][col] == 2
        if col - 1 >= 0:
            left = self.matrix[row][col - 1] == 1
        if col + 1 < self.n:
            right = self.matrix[row][col + 1] == 1
        return up, down, left, right

    def board_to_graph(self):
        graph = {}
        for i in range(self.n):
            for j in range(self.n):
                graph[(i, j)] = []
                left_c, right_c, up_c, down_c = self.get_connections(i, j)
                if self.matrix[i][j] == 1:
                    if left_c:
                        graph[(i, j)].append((i, j - 1))
                    if right_c:
                        graph[(i, j)].append((i, j + 1))
                elif self.matrix[i][j] == 2:
                    if up_c:
                        graph[(i, j)].append((i - 1, j))
                    if down_c:
                        graph[(i, j)].append((i + 1, j))
                elif self.matrix[i][j] == 3:
                    if up_c:
                        graph[(i, j)].append((i - 1, j))
                    if right_c:
                        graph[(i, j)].append((i, j + 1))
                elif self.matrix[i][j] == 4:
                    if right_c:
                        graph[(i, j)].append((i, j + 1))
                    if down_c:
                        graph[(i, j)].append((i + 1, j))
                elif self.matrix[i][j] == 5:
                    if down_c:
                        graph[(i, j)].append((i + 1, j))
                    if left_c:
                        graph[(i, j)].append((i, j - 1))
                elif self.matrix[i][j] == 6:
                    if left_c:
                        graph[(i, j)].append((i, j - 1))
                    if up_c:
                        graph[(i, j)].append((i - 1, j))
        return graph

    def get_connections(self, i, j):
        left_c, right_c, up_c, down_c = False, False, False, False
        if i - 1 >= 0:
            up_c = self.matrix[i - 1][j] == 2 or self.matrix[i - 1][j] == 4 or self.matrix[i - 1][j] == 5
        if i + 1 < self.n:
            down_c = self.matrix[i + 1][j] == 2 or self.matrix[i + 1][j] == 3 or self.matrix[i + 1][j] == 6
        if j - 1 >= 0:
            left_c = self.matrix[i][j - 1] == 1 or self.matrix[i][j - 1] == 3 or self.matrix[i][j - 1] == 4
        if j + 1 < self.n:
            right_c = self.matrix[i][j + 1] == 1 or self.matrix[i][j + 1] == 5 or self.matrix[i][j + 1] == 6
        return left_c, right_c, up_c, down_c

    def print_graph(self, graph):
        for key in graph:
            print(str(key) + " -> " + str(graph[key]))

    def verify_cycle(self, graph):
        visited = set()
        stack = []
        start_node = self.find_start_point()
        stack.append((start_node, None))  # Usamos una tupla para rastrear el nodo y su padre
        while stack:
            node, parent = stack.pop()
            visited.add(node)
            neighbours = graph[node]
            for neighbour in neighbours:
                if neighbour not in visited:
                    stack.append((neighbour, node))  # Agregamos el nodo y su padre a la pila
                elif neighbour != parent:  # Verificamos que el vecino no sea el padre del nodo actual
                    return True  # Si encontramos un ciclo, devolvemos True
        return False  # Si no encontramos ciclos, devolvemos False
    # End def
# End class
