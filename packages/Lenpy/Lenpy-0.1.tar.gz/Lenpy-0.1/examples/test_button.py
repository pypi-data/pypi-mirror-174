
import pygame, os, sys
import lenpy

pygame.init()

# Colores
WHITE = pygame.Color("#ffffff")
BLACK = pygame.Color("#000000")
RED = pygame.Color("#FF0000")
GREEN = pygame.Color("#25914C")
BLUE = pygame.Color("#0000FF")

# Tamaño de la pantalla
screen_size = [800, 480]

screen = lenpy.config.set_display(screen_size)

pygame.display.set_caption("Test Len'Py Button")

# Localiza el directorio de ejecución
source_dir = os.path.split(os.path.abspath(__file__))[0]

buttontext_a = lenpy.ui.TextButton("Boton", "arial.ttf", 24, "#FF0000", "#25914C", "#0000FF", "quit", font_dir=f"{source_dir}\\fonts\\")

buttontext_b = lenpy.ui.TextButton("Otro boton", "arial.ttf", 24, "#FF0000", "#25914C", "#0000FF", True, font_dir=f"{source_dir}\\fonts\\")

while True:
    
    # Obtiene los eventos
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    # Dibuja los textos
    buttontext_a.draw(screen, 20, 20)
    buttontext_b.draw(screen, 400, 20)
    
    pygame.display.flip()
    lenpy.config.clock.tick(60)