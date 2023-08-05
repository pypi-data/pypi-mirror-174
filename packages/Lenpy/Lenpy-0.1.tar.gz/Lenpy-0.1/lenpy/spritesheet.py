
# Un modulo para usar Sprite XML hechos con Adobe Flash CS6 o Adobe Animate

import pygame
import xml.etree.ElementTree as ET
from lenpy import tools

pygame.init()

class SpriteSheet():
   
    def __init__(self, img_file, data_file=None):

        # Define las variables
        self.spritesheet = pygame.image.load(img_file).convert_alpha() # Carga la imagen
        self.ajustement = False
        self.frame_index = 0
        self.fps = 0
        self.frames = []
        self.update_time = pygame.time.get_ticks()
        self.img = None
        self.rect = None
        self.not_repeat = False

        if data_file:
        
            tree = ET.parse(data_file)
        
            self.map = {}
        
            for node in tree.iter():

                # node obtendra.attrib contiene toda la información a usar de los sprites XML, por ejemplo el nombre

                if node.attrib.get('name'):
                    
                    # Carga los nombres de las animaciones
                    name = node.attrib.get('name')

                    # Asigna los atributos(x,y, etc.) de las animaciones en self.map
                    self.map[name] = {}
                    self.map[name]['x'] = int(node.attrib.get('x'))
                    self.map[name]['y'] = int(node.attrib.get('y'))
                    self.map[name]['width'] = int(node.attrib.get('width'))
                    self.map[name]['height'] = int(node.attrib.get('height'))

                    # Si el XML contiene los atributos 'frameX','frameY','frameWidth', 'frameHeight'

                    if "frameX" and "frameY" and "frameWidth" and "frameHeight" in node.attrib:
                        
                        self.map[name]['frameX'] = int(node.attrib.get('frameX'))
                        self.map[name]['frameY'] = int(node.attrib.get('frameY'))
                        self.map[name]['frameWidth'] = int(node.attrib.get('frameWidth'))
                        self.map[name]['frameHeight'] = int(node.attrib.get('frameHeight'))

                        self.ajustement = True

                        # NOTA: No recomiendo usar los sprites XML con estos atributos, debido a que tengo que buscar la forma
                        # de que los fotogramas queden centrados y no se muevan, si quieres puedes probar y ver lo que pasa.
    
    def get_image_rect(self, x, y, w, h):
        
        # Retorna la imagen pero con su respectivo recorte, es decir sin mostrar toda la imagen
        return self.spritesheet.subsurface(pygame.Rect(x, y, w, h))

    def get_image_name(self, name):

        # Esta ajustada?
        if self.ajustement == True:

            fw = self.map[name]['width'] // self.map[name]['frameWidth']
            fh = self.map[name]['height'] // self.map[name]['frameHeight']
            
            rect = pygame.Rect(self.map[name]['x'], self.map[name]['y'], self.map[name]['width'] - fw , self.map[name]['height'] - fh)
        
        else:
            
            rect = pygame.Rect(self.map[name]['x'], self.map[name]['y'], self.map[name]['width'] , self.map[name]['height'])
        
        # Retorna la animación
        return self.spritesheet.subsurface(rect)

    def get_animation_name(self, n:str, frames_amount):

        self.frame_index = 0

        num = tools.numbers_Count(0, 0, 0, 0)

        self.frames = []

        # Cuantos fotogramas tiene tu animación?
        for spr_name in range(frames_amount):

            numbers = num.count()
            name = n + numbers
            num.d += 1 

            # Agrega la animación
            self.frames.append(name)

        img = self.frames[self.frame_index]

        self.img = self.get_image_name(img)

    def update(self, fps, repeat=True):

        self.fps = fps

        img = self.frames[self.frame_index]

        self.img = self.get_image_name(img)

        if repeat == True:
            self.not_repeat = False

        if self.not_repeat == True:

            self.frame_index = 0

        elif not self.not_repeat:

            # Si los fotogramas de la pantalla son iguales a la velocidad de la animación, entonces...
            if pygame.time.get_ticks() - self.update_time > self.fps:

                self.update_time = pygame.time.get_ticks()
                self.frame_index +=1

            # Si el indice se pasa, entonces...
            if self.frame_index > len(self.frames) - 1:

                self.frame_index = 0

                if repeat == False:
                    self.not_repeat = True

    def draw(self, surface, x, y, scale=1.0):

        img_ok = pygame.transform.scale(self.img, (self.img.get_width() * scale, self.img.get_height() * scale))

        # Obtiene el rectangulo de la imagen
        self.rect = img_ok.get_rect()

        if self.ajustement == True:

            # Esto no funciona todavia
            self.rect.center = [x - self.map[self.img].get("frameX"), y - self.map[self.img].get("frameY")]

        else:
            self.rect.center = [x, y]

        # Dibuja la imagen
        surface.blit(img_ok, self.rect)