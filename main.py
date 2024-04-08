import sys

from board import read_input_file, Board
from graphic_interface import GUI
from menu import Menu


def main(input_file):
    # Mostrar menú
    menu = Menu()
    menu.run()
    try:
        n, pearls = read_input_file(input_file)
        if n == 0 or len(pearls) == 0:
            print("The input file is empty")
            exit(1)
    except:
        print("Error reading the input file")
        exit(1)

    board = Board(n, pearls)
    gui = GUI(board)
    try:
        gui.run()
    except KeyboardInterrupt:
        pass
    # End try
# End def


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ", sys.argv[0], "input_file")
        exit(1)
    main(sys.argv[1])
# End if
