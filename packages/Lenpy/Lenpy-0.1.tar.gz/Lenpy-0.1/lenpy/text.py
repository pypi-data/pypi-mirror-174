
# Una forma un poco más sencilla de pintar texto en la pantalla

import pygame, os
from lenpy import locals

pygame.font.init()

class Text():
    def __init__(self, text:str, font_name:str, size:int, font_dir=None, color=None, antialias=True, background=None, italic=False, bold=False, underline=False, xcenter=False, ycenter=False, sysfont=False):

        # Define las variables
        self.text = text
        self.text_img = []
        self.font_name = font_name
        self.size = size
        self.font_dir = font_dir
        self.x = int
        self.y = int
        self.color = color
        self.antialias = antialias
        self.background = background
        self.italic = italic
        self.bold = bold
        self.underline = underline
        self.xcenter = xcenter
        self.ycenter = ycenter
        self.sysfont = sysfont
        self.font = []

        # Si sysfont es True, Len'Py usara la función SysFont de pygame para cargar la fuente.
        if not self.sysfont:

            if self.font_dir:
                
                self.font = pygame.font.Font(f"{self.font_dir}\\{self.font_name}", self.size)

        else:

            self.font = pygame.font.SysFont(self.font_name, self.size)


    def draw(self, surface, x:int, y:int):

        font = self.font

        if self.underline:
            font.set_underline(True)

        if self.bold:
            font.set_bold(True)

        if self.italic:
            font.set_italic(True)

        text = font.render(self.text, self.antialias, self.color, self.background)

        self.text_img = text

        if self.xcenter:
            self.x = (surface.get_width() // 2) - (text.get_width() // 2)
        
        else:
            self.x = x
        
        if self.ycenter:
            self.y = (surface.get_height() // 2) - (text.get_height() // 2)
        
        else:
            self.y = y

        # Dibuja el texto en la pantalla
        surface.blit(self.text_img, [self.x, self.y])

    def get_text_rect(self):

        surface = self.font.render(self.text, self.antialias, self.color, self.background)
        rect = surface.get_rect()

        return rect