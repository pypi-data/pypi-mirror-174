
# Una prueba sencilla para probar la capacidad del modulo Spritesheet

import pygame, os, sys
import lenpy

# Localiza el directorio de ejecución
source_dir = os.path.split(os.path.abspath(__file__))[0]

pygame.init()

# El tamaño de la pantalla
screen_size = [800, 480]

screen = lenpy.config.set_display(screen_size)

pygame.display.set_caption("Test Ball SpriteSheet XML")

class Ball():
    
    def __init__(self, x, y):
        
        # define las variables a usar

        self.x = x
        self.y = y
        self.animation = []
        self.animation_name = "" # El nombre de la animación actual
        self.scale = 1.0

        # Importamos la imagen y su respectivo archivo 'xml'
        
        ball = lenpy.spritesheet.SpriteSheet(f"{source_dir}\\xml_sprite_example\\ball_example.png", f"{source_dir}\\xml_sprite_example\\ball_example.xml")
            
        self.ball = ball

        self.idle()
    
    def idle(self):

        # Regresa los fotogramas a cero
        self.ball.frame_index = 0

        self.animation_name = "idle"
        
        self.animation = self.ball.get_animation_name("Ball", 4)

    def move(self, key=None):

        # Regresa de nuevo, los fotogramas a cero
        
        self.ball.frame_index = 0

        if key == "up":
   
            self.animation = self.ball.get_animation_name("Ball Up", 1)
            self.animation_name = "up"

        elif key == "down":

            self.animation = self.ball.get_animation_name("Ball Down", 1)
            self.animation_name = "down"

        elif key == "left":

            self.animation = self.ball.get_animation_name("Ball Left", 1)
            self.animation_name = "left"

        elif key == "right":

            self.animation = self.ball.get_animation_name("Ball Right", 1)
            self.animation_name = "right"

        elif key == None:

            self.idle()

    def update(self):

        fps = 24 # Velocidad de los fotogramas, usualmente es 24
        
        self.ball.update(fps)


    def draw(self, surface, x, y):

        if self.animation_name == "idle":

            self.ball.draw(surface, x, y, self.scale)

        elif self.animation_name == "up":
           
            self.ball.draw(surface, x, y-20, self.scale)

        elif self.animation_name == "down":
           
            self.ball.draw(surface, x, y+20, self.scale)

        elif self.animation_name == "right":
           
            self.ball.draw(surface, x+20, y, self.scale)

        elif self.animation_name == "left":
           
            self.ball.draw(surface, x-20, y, self.scale)

        # Los 20 que se suman o restan a las coordenadas de la pelota es para poder ajustar todas las animaciones, la cantidad 
        # a sumar o restar dependera del sprite

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