import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 480, 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_WIDTH = 5
ROWS, COLS = 6, 6
SQUARE_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Masyu con Pygame")

# Representación del tablero
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Lista de direcciones de movimiento (arriba, abajo, izquierda, derecha)
MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Función para dibujar el tablero
def draw_board():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            if board[row][col] == 1:
                pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), LINE_WIDTH // 2)

# Función para verificar si una casilla está dentro del tablero
def is_valid(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

# Función para verificar si una línea entre dos puntos es válida
def is_valid_line(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    # Verificar que la línea sea horizontal o vertical
    if dx != 0 and dy != 0:
        return False

    # Verificar que la línea no cruce ningún círculo
    for i in range(1, max(abs(dx), abs(dy))):
        row = start[0] + i * (dy // max(abs(dx), abs(dy)))
        col = start[1] + i * (dx // max(abs(dx), abs(dy)))
        if board[row][col] == 1:
            return False

    return True

# Función para verificar si el juego ha sido completado
def is_game_complete():
    # Verificar que todos los círculos están conectados por líneas
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 1:
                connected = False
                for move in MOVES:
                    new_row = row + move[0]
                    new_col = col + move[1]
                    if is_valid(new_row, new_col) and board[new_row][new_col] == 2:
                        if is_valid_line((row, col), (new_row, new_col)):
                            connected = True
                            break
                if not connected:
                    return False
    return True

# Bucle principal del juego
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    row = event.pos[1] // SQUARE_SIZE
                    col = event.pos[0] // SQUARE_SIZE
                    if is_valid(row, col):
                        if board[row][col] == 0:
                            board[row][col] = 1
                        elif board[row][col] == 1:
                            board[row][col] = 2
                        elif board[row][col] == 2:
                            board[row][col] = 0

                        if is_game_complete():
                            print("¡Felicidades! Has completado el juego.")

        draw_board()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
