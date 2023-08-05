
import pygame
import os

pygame.init()

# Hay una forma más sencilla de hacer un conteo de 4 digitos?
# Esta clase permite un conteo de 4 digitos, usando la función Count()

class numbers_Count():

    def __init__(self, a, b, c, d):

        self.a = a
        self.b = b
        self.c = c
        self.d = d
    
    def count(self):

        if self.d == 10:

            self.c += 1
            self.d = 0

            if self.c == 10:

                self.b += 1
                self.c = 0

                if self.b == 10:

                    self.a += 1
                    self.b = 0

                    if self.a == 10:

                        self.a = 0

        a = str(self.a)
        b = str(self.b)
        c = str(self.c)
        d = str(self.d)

        numbers = a + b + c + d

        return numbers


# num = numbers_Count(0, 0, 0, 0)

# for i in range(10):

#   numbers = num.count()
#   num.d += 1
#   print(numbers)


# Una forma de definir animaciones de multiples imagenes, pero por ahora solo permite imagenes cuyo nombre contiene 4 digitos.

def define_animations(frames_amount, d, dir_name, name, anim_name):

    # Al exportar una secuencia de imagenes en Adobe Flash o Animate, la secuencia de imagenes tiene el nombre y 4 digitos
    
    # frames_amount: Cuantas imagenes tiene la animación, si tiene 25 coloca 26, siempre un número más.
    # d: Donde están las imagenes, assets\images?
    # dir_name: Enemy?
    # name: idle, attack?
    # anim_name: si la animación es idle, usualmente inicial de la animación es idle

    temp_list = []

    num = numbers_Count(0, 0, 0 , 1)

    for i in range(frames_amount):

        numbers = num.count()
        
        if i > 0:

            num.d += 1

        # Carga la imagen
        image = pygame.image.load(f"{d}\\{dir_name}\\{name}\\{anim_name}{numbers}.png").convert_alpha()
        img = pygame.transform.scale(image, (image.get_width(), image.get_height()))
                   
        temp_list.append(img)

    return temp_list

# Crea un directorio de una forma más sencilla, aunque creo que ya es sencilla la forma de crearlos, no?

def make_dir(d:str, name:str):

    if name and d:
        
        os.makedirs(d + "/" + name, exist_ok=True)