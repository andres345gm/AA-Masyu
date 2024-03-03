from board import read_input_file, Board
from graphic_interface import GUI
from menu import Menu


def main():
    # Mostrar menú
    menu = Menu()
    menu.run()

    n, pearls = read_input_file("input01.txt")
    board = Board(n, pearls)
    gui = GUI(board)
    try:
        gui.run()
    except KeyboardInterrupt:
        pass
    # End try
# End def


if __name__ == "__main__":
    main()
