
# Una prueba sencilla por si tienes muchas imagenes para una animación

import pygame, os, sys
import lenpy

# Localiza el directorio de ejecución
source_dir = os.path.split(os.path.abspath(__file__))[0]

pygame.init()

# El tamaño de la pantalla
screen_size = [800, 480]

screen = lenpy.config.set_display(screen_size)

pygame.display.set_caption("Test Ball Multiple Images")

class Ball():
    
    def __init__(self, x, y):
        
        # define las variables a usar

        self.x = x
        self.y = y
        self.animation = []
        self.animation_name = "" # El nombre de la animación actual
        self.scale = 1.0
        self.animations_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #cargar imagenes
        temp_list = []
        temp_list = lenpy.tools.define_animations(5, source_dir, "multiple_images_example", "idle", "Ball")
        self.animations_list.append(temp_list)

        temp_list = []
        temp_list = lenpy.tools.define_animations(3, source_dir, "multiple_images_example", "up", "Ball Up")
        self.animations_list.append(temp_list)

        temp_list = []
        temp_list = lenpy.tools.define_animations(3, source_dir, "multiple_images_example", "down", "Ball Down")
        self.animations_list.append(temp_list)

        temp_list = []
        temp_list = lenpy.tools.define_animations(3, source_dir, "multiple_images_example", "left", "Ball Left")
        self.animations_list.append(temp_list)

        temp_list = []
        temp_list = lenpy.tools.define_animations(3, source_dir, "multiple_images_example", "right", "Ball Right")
        self.animations_list.append(temp_list)

        self.image = self.animations_list[self.action][self.frame_index]

    def update(self):

        animation_cooldown = 60

        # actualizar imagen
        self.image = self.animations_list[self.action][self.frame_index]
        
        # chequear si ya se paso la actualización de la pantalla
        
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1

        # Que pasa si la animación se sale del rango
        
        if self.frame_index >= len(self.animations_list[self.action]):
            
            self.frame_index = 0

    def idle(self):

        # Regresa los fotogramas a cero
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def move(self, key=None):

        # Regresa de nuevo, los fotogramas a cero
        
        self.frame_index = 0

        if key == "up":
   
            self.action = 1

        elif key == "down":

            self.action = 2

        elif key == "left":

            self.action = 3

        elif key == "right":

            self.action = 4

        elif key == None:

            self.idle()

    def draw(self, surface, x, y):

        self.rect = self.image.get_rect()

        if self.action == 0:

            self.rect.center = [x, y]

        elif self.action == 1:
           
            self.rect.center = [x, y-20]

        elif self.action == 2:
           
            self.rect.center = [x, y+20]

        elif self.action == 3:
           
            self.rect.center = [x-20, y]

        elif self.action == 4:
           
            self.rect.center = [x+20, y]

        surface.blit(self.image, self.rect)

WHITE = pygame.Color("#ffffff")

# Coordenadas iniciales
coord_x = 320
coord_y = 220

# Velocidad inicial
speed = [0, 0]

ball = Ball(coord_x, coord_y)

while True:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            
            # Mueve la pelota
            if event.key == pygame.K_LEFT:
                speed[0] = -5
                ball.move(key="left")

            elif event.key == pygame.K_RIGHT:
                speed[0] = 5
                ball.move(key="right")

            elif event.key == pygame.K_UP:
                speed[1] = -5
                ball.move(key="up")

            elif event.key == pygame.K_DOWN:
                speed[1] = 5
                ball.move(key="down")

            if event.key == pygame.K_PLUS:
                ball.scale += 0.2

            elif event.key == pygame.K_MINUS:
                ball.scale -= 0.2
        
        if event.type == pygame.KEYUP:
            
            # Si no se esta pulsando una tecla, la pelota no se mueve.
            if event.key == pygame.K_LEFT:
                speed[0] = 0
                ball.move(key=None)

            elif event.key == pygame.K_RIGHT:
                speed[0] = 0
                ball.move(key=None)

            elif event.key == pygame.K_UP:
                speed[1] = 0
                ball.move(key=None)

            elif event.key == pygame.K_DOWN:
                speed[1] = 0
                ball.move(key=None)
    
    # Rellena la pantalla
    screen.fill(WHITE)

    coord_x += speed[0]
    coord_y += speed[1]

    # Dibuja la pelota con los valores actuales de las variables 'coord_x' y 'coord_y'
    ball.draw(screen, coord_x, coord_y)

    # Actualiza los fotogramas de la pelota
    ball.update()

    pygame.display.flip()
    lenpy.config.clock.tick(60)