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
    def __init__(self, n, pearls):
        self.n = n
        self.matrix = [[0 for _ in range(n)] for _ in range(n)]
        for pearl in pearls:
            self.matrix[pearl[0] - 1][pearl[1] - 1] = pearl[2]
        # End for
    # End def

# End class
