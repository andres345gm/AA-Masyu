import pygame
import sys
import textwrap


class Menu:
    # Constantes
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (240, 148, 64)
    LIGHT_ORANGE = (240, 179, 106)
    WIDTH, HEIGHT = 480, 480
    MENU_FONT_SIZE = 24
    INSTRUCTIONS_FONT_SIZE = 16

    def __init__(self):
        self.screen = None
    # End def

    def show_menu(self):
        # Se inicializa pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Masyu con Pygame")
        self.screen.fill(self.WHITE)

        # Se definen los colores de los botones
        button_color = self.ORANGE
        hover_color = self.LIGHT_ORANGE

        # Se definen las posiciones y tamaños de los botones
        button_width = 200
        button_height = 50
        button_spacing = 20
        total_button_height = (button_height + button_spacing) * 4
        top_margin = (self.HEIGHT - total_button_height) // 2

        # Se dibujan las opciones del menú
        font = pygame.font.SysFont(None, self.MENU_FONT_SIZE)

        # Opción de Jugar
        play_button_rect = pygame.Rect((self.WIDTH - button_width) // 2, top_margin, button_width, button_height)
        pygame.draw.rect(self.screen, button_color, play_button_rect)
        play_text = font.render("Jugar", True, self.BLACK)
        play_text_rect = play_text.get_rect(center=play_button_rect.center)
        self.screen.blit(play_text, play_text_rect)

        # Opción de Instrucciones
        instructions_button_rect = play_button_rect.move(0, (button_height + button_spacing))
        pygame.draw.rect(self.screen, button_color, instructions_button_rect)
        instructions_text = font.render("Instrucciones", True, self.BLACK)
        instructions_text_rect = instructions_text.get_rect(center=instructions_button_rect.center)
        self.screen.blit(instructions_text, instructions_text_rect)

        # Opción de Salir
        quit_button_rect = play_button_rect.move(0, (button_height + button_spacing) * 2)
        pygame.draw.rect(self.screen, button_color, quit_button_rect)
        quit_text = font.render("Salir", True, self.BLACK)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        self.screen.blit(quit_text, quit_text_rect)

        # Se actualiza la pantalla
        pygame.display.flip()

        # Bucle principal para elegir opción
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # End if
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    # Cambiar el color cuando el mouse pasa sobre los botones
                    # Boton de Jugar
                    if play_button_rect.collidepoint(x, y):
                        pygame.draw.rect(self.screen, hover_color, play_button_rect)
                    # End if
                    else:
                        pygame.draw.rect(self.screen, button_color, play_button_rect)
                    # End else

                    # Boton de Instrucciones
                    if instructions_button_rect.collidepoint(x, y):
                        pygame.draw.rect(self.screen, hover_color, instructions_button_rect)
                    # End if
                    else:
                        pygame.draw.rect(self.screen, button_color, instructions_button_rect)
                    # End else

                    # Boton de Salir
                    if quit_button_rect.collidepoint(x, y):
                        pygame.draw.rect(self.screen, hover_color, quit_button_rect)
                    # End if
                    else:
                        pygame.draw.rect(self.screen, button_color, quit_button_rect)
                    # End else

                    # Volver a dibujar los textos
                    self.screen.blit(play_text, play_text_rect)
                    self.screen.blit(instructions_text, instructions_text_rect)
                    self.screen.blit(quit_text, quit_text_rect)

                    pygame.display.flip()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # Opción de Jugar
                    if play_button_rect.collidepoint(x, y):
                        return "Jugar"
                    # End if
                    # Opción de Instrucciones
                    elif instructions_button_rect.collidepoint(x, y):
                        # Lógica para las instrucciones
                        self.show_instructions()
                        self.show_menu()
                        pass
                    # End if

                    # Opción de Salir
                    elif quit_button_rect.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()
                    # End if
                # End elif
            # End for
        # End while
    # End def

    def show_instructions(self):
        self.screen.fill(self.WHITE)

        # Define the instructions text
        instructions = [
            "- Haz un solo recorrido con líneas que pasen por el centro de las celdas, ya sea horizontal o verticalmente. El recorrido nunca se cruza a sí mismo, se ramifica ni pasa por la misma celda dos veces.",
            "- Las líneas deben pasar por todas las celdas con círculos negros y blancos.",
            "- Las líneas que pasan por círculos blancos deben atravesar directamente su celda y hacer un giro en ángulo recto en al menos una de las celdas adyacentes al círculo blanco.",
            "- Las líneas que pasan por círculos negros deben hacer un giro en ángulo recto en su celda, luego deben ir rectas a través de la siguiente celda (hasta el centro de la segunda celda) en ambos lados.",
            "- Linea Vertical: Click Izquierdo, Linea Horizontal: Click Derecho, Curva 90°: Tecla 'C'"
        ]

        # Define the back button
        back_button_text = "Volver"
        back_button_rect = pygame.Rect((self.WIDTH - 200) // 2, self.HEIGHT - 70, 200, 50)

        # Draw the instructions text
        font = pygame.font.SysFont(None, self.INSTRUCTIONS_FONT_SIZE, bold=False)
        y = 50
        for instruction in instructions:
            lines = textwrap.wrap(instruction, width=80)
            for line in lines:
                text = font.render(line, True, self.BLACK)
                text_rect = text.get_rect(center=(self.WIDTH // 2, y))
                self.screen.blit(text, text_rect)
                y += 30

        # Draw the back button
        pygame.draw.rect(self.screen, self.ORANGE, back_button_rect)
        back_text = font.render(back_button_text, True, self.BLACK)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)

        pygame.display.flip()

        # Handle mouse events
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if back_button_rect.collidepoint(x, y):
                        return

    def run(self):
        while True:
            choice = self.show_menu()
            # Si se elige Jugar, simplemente retorna y se sigue con el main
            if choice == "Jugar":
                return
            # End if
        # End while
    # End def

# End class
