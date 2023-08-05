
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

pygame.display.set_caption("Test Len'Py Text")

# Localiza el directorio de ejecución
source_dir = os.path.split(os.path.abspath(__file__))[0]

# Almacena los textos a mostrar en una variable
text_a = lenpy.Text("Hola Mundo!!!", "arial.ttf", 24, f"{source_dir}\\fonts\\", BLACK, sysfont=False)
text_b = lenpy.Text("Hola Mundo!!!", "comic sans", 24, None, RED, sysfont=True)
text_c = lenpy.Text("Hola Mundo!!!", "serif", 24, None, GREEN, sysfont=True)

i = 100

while True:
    
    # Obtiene los eventos
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    i += 2

    # Dibuja los textos
    text_a.draw(screen, 20, 20)
    text_b.draw(screen, 20, 60)
    text_c.draw(screen, 20, i)
    
    pygame.display.flip()
    lenpy.config.clock.tick(60)