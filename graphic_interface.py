import time

import pygame
import sys


class GUI:
    # Constantes
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (240, 148, 64)
    WIDTH, HEIGHT = 480, 480
    LINE_WIDTH = 3
    BUTTON_WIDTH, BUTTON_HEIGHT = 480, 50

    def __init__(self, board):
        self.board = board
        self.square_size = self.WIDTH // self.board.n
        self.c_value = 3
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT + self.BUTTON_HEIGHT))
        pygame.display.set_caption("Masyu con Pygame")
        self.solution_button_rect = pygame.Rect((self.WIDTH - self.BUTTON_WIDTH) // 2, self.HEIGHT, self.BUTTON_WIDTH,
                                                self.BUTTON_HEIGHT)
    # End def

    def draw_board(self):
        self.screen.fill(self.WHITE)
        for row in range(self.board.n):
            for col in range(self.board.n):
                pygame.draw.rect(self.screen, self.BLACK,
                                 (col * self.square_size, row * self.square_size, self.square_size, self.square_size),
                                 1)
                if self.board.pearls[row][col] == 1:
                    self.draw_circle(row, col, self.WHITE)
                elif self.board.pearls[row][col] == 2:
                    self.draw_circle(row, col, self.BLACK)

                if self.board.matrix[row][col] == 1:
                    self.draw_line(row, col, 'horizontal')
                elif self.board.matrix[row][col] == 2:
                    self.draw_line(row, col, 'vertical')
                elif self.board.matrix[row][col] == 3:
                    self.draw_line(row, col, 'up_right')
                elif self.board.matrix[row][col] == 4:
                    self.draw_line(row, col, 'down_right')
                elif self.board.matrix[row][col] == 5:
                    self.draw_line(row, col, 'down_left')
                elif self.board.matrix[row][col] == 6:
                    self.draw_line(row, col, 'up_left')
                # End if
            # End for
        # End for
        pygame.draw.rect(self.screen, self.ORANGE, self.solution_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("Solución", True, self.BLACK)
        text_rect = text.get_rect(center=self.solution_button_rect.center)
        self.screen.blit(text, text_rect)
        pygame.display.flip()  # Update the full display Surface to the screen

    # End def

    def draw_circle(self, row, col, color):
        # Se calcula el centro del círculo
        center_x = col * self.square_size + self.square_size // 2
        center_y = row * self.square_size + self.square_size // 2
        # Se calcula el radio del círculo
        radius = self.square_size // 4  # Circle's inner radius

        # Se dibuja el círculo
        border_thickness = 2  # You can adjust the thickness of the border here
        # Se dibuja el círculo más grande
        pygame.draw.circle(self.screen, self.BLACK, (center_x, center_y), radius + border_thickness)
        # Se dibuja el círculo más pequeño
        pygame.draw.circle(self.screen, color, (center_x, center_y), radius)

    # End def

    def draw_line(self, row, col, orientation):
        # Define start, end points and center for the line within the cell
        start_point = (col * self.square_size, row * self.square_size)
        end_point = ((col + 1) * self.square_size, (row + 1) * self.square_size)
        center = ((col + 0.5) * self.square_size, (row + 0.5) * self.square_size)

        if orientation == 'horizontal':
            # Dibuja la línea horizontal en el medio de la celda
            pygame.draw.line(self.screen, self.BLACK, (start_point[0], start_point[1] + self.square_size // 2),
                             (end_point[0], start_point[1] + self.square_size // 2), self.LINE_WIDTH)
        elif orientation == 'vertical':
            # Dibuja la línea vertical en el medio de la celda
            pygame.draw.line(self.screen, self.BLACK, (start_point[0] + self.square_size // 2, start_point[1]),
                             (start_point[0] + self.square_size // 2, end_point[1]), self.LINE_WIDTH)
        elif orientation == 'up_right':
            end_point = (center[0] + self.square_size // 2, center[1])
            pygame.draw.line(self.screen, self.BLACK, center, end_point, self.LINE_WIDTH)
            pygame.draw.line(self.screen, self.BLACK, center, (center[0], center[1] - self.square_size // 2),
                             self.LINE_WIDTH)
        elif orientation == 'down_right':
            end_point = (center[0], center[1] + self.square_size // 2)
            pygame.draw.line(self.screen, self.BLACK, center, end_point, self.LINE_WIDTH)
            pygame.draw.line(self.screen, self.BLACK, center, (center[0] + self.square_size // 2, center[1]),
                             self.LINE_WIDTH)
        elif orientation == 'down_left':
            end_point = (center[0] - self.square_size // 2, center[1])
            pygame.draw.line(self.screen, self.BLACK, center, end_point, self.LINE_WIDTH)
            pygame.draw.line(self.screen, self.BLACK, center, (center[0], center[1] + self.square_size // 2),
                             self.LINE_WIDTH)
        elif orientation == 'up_left':
            end_point = (center[0], center[1] - self.square_size // 2)
            pygame.draw.line(self.screen, self.BLACK, center, end_point, self.LINE_WIDTH)
            pygame.draw.line(self.screen, self.BLACK, center, (center[0] - self.square_size // 2, center[1]),
                             self.LINE_WIDTH)
        # End if

    # End def

    def display_message(self, message):
        # Create a new surface for the background
        background = pygame.Surface((self.WIDTH // 1.5, self.HEIGHT // 4), pygame.SRCALPHA)
        # Fill the surface with a semi-transparent orange color
        background.fill((*self.ORANGE, 128))  # 128 is the alpha value (semi-transparent)
        background_rect = background.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(background, background_rect)

        font = pygame.font.Font(None, 36)
        text = font.render(message, True, self.BLACK)
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.solution_button_rect.collidepoint(x, y):
                        start = time.time()
                        solution = self.board.solve_board()
                        end = time.time()
                        print("Tiempo de ejecución: ", end - start)
                        if solution is not None:
                            self.board.matrix = solution
                            self.draw_board()
                            pygame.display.flip()
                            self.display_message("¡Solución encontrada!")
                            pygame.time.wait(1000)
                        else:
                            self.draw_board()
                            pygame.display.flip()
                            self.display_message("¡Solución no encontrada!")
                            pygame.time.wait(1000)
                        self.draw_board()
                        pygame.display.flip()
                    else:
                        row = event.pos[1] // self.square_size
                        col = event.pos[0] // self.square_size
                        if event.button == 1:  # Left click
                            self.board.matrix[row][col] = 2
                        elif event.button == 3:  # Right click
                            self.board.matrix[row][col] = 1
                        elif event.button == 2:
                            self.board.matrix[row][col] = 0
                        # End if
                        if self.board.verify_board():
                            self.draw_board()
                            pygame.display.flip()
                            self.display_message("¡Has ganado!")
                            pygame.time.wait(1000)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # Tecla C
                        # Incrementar el valor y guardarlo en la matriz
                        row = pygame.mouse.get_pos()[1] // self.square_size
                        col = pygame.mouse.get_pos()[0] // self.square_size
                        self.board.matrix[row][col] = self.c_value
                        # print("Click en la celda ({}, {})".format(row, col))
                        # print(self.board.matrix)
                        self.c_value += 1
                        if self.c_value > 6:  # Si llega a 7, reiniciar en 3
                            self.c_value = 3

                        if self.board.verify_board():
                            self.draw_board()
                            pygame.display.flip()
                            self.display_message("¡Has ganado!")
                            pygame.time.wait(1000)
                # End if
            # End for
            self.draw_board()
            pygame.display.flip()  # Actualiza la pantalla
        # End while
        pygame.quit()
        sys.exit()
    # End def
# End class
