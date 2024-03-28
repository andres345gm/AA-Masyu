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

    def verify_solution(self):
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
        return True
    # End def

    def verify_white_pearl(self, row, col):
        # Verification if the line is horizontal
        if col - 1 >= 0 and col + 1 < self.n:
            if self.matrix[row][col] == 1:
                is_straight = self.matrix[row][col - 1] == 1 and self.matrix[row][col + 1] == 1
                left_turn = self.matrix[row - 1][col - 1] == 2 or self.matrix[row + 1][col - 1] == 2
                right_turn = self.matrix[row - 1][col + 1] == 2 or self.matrix[row + 1][col + 1] == 2
                return is_straight and (left_turn or right_turn)
            # End if
        if row - 1 >= 0 and row + 1 < self.n:
            # Verification if the line is vertical
            if self.matrix[row][col] == 2:
                is_straight = self.matrix[row - 1][col] == 2 and self.matrix[row + 1][col] == 2
                top_turn = self.matrix[row - 1][col - 1] == 1 or self.matrix[row - 1][col + 1] == 1
                bottom_turn = self.matrix[row + 1][col - 1] == 1 or self.matrix[row + 1][col + 1] == 1
                return is_straight and (top_turn or bottom_turn)
            # End if
        return False

    # end def

    def verify_black_pearl(self, row, col):
        up, down, left, right = self.get_neighbours(row, col)
        if up and right:
            if row - 1 >= 0 and col + 1 < self.n:
                return self.matrix[row][col + 1] == 1 and self.matrix[row - 1][col] == 2
            # end if
        elif up and left:
            if row - 1 >= 0 and col - 1 >= 0:
                return self.matrix[row][col - 1] == 1 and self.matrix[row - 1][col] == 2
            # end if
        elif down and right:
            if row + 1 < self.n and col + 1 < self.n:
                return self.matrix[row][col + 1] == 1 and self.matrix[row + 1][col] == 2
            # end if
        elif down and left:
            if row + 1 < self.n and col - 1 >= 0:
                return self.matrix[row][col - 1] == 1 and self.matrix[row + 1][col] == 2
            # end if
        # end if

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

# End class
