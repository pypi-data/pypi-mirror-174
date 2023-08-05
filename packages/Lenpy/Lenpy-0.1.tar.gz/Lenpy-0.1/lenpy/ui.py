
import pygame, sys
from lenpy.text import Text 

class TextButton():
    
    def __init__(self, text:str, font:str, size:int, normal_color:str, select_color:str, hover_color:str, action=None, font_dir=None, italic=False, bold=False, underline=False, sysfont=False):

        self.x = int
        self.y = int
        self.font = font
        self.font_dir = font_dir
        self.size = size
        self.normal_color = normal_color
        self.select_color = select_color
        self.hover_color = hover_color
        self.action = []
        self.get_action = action
        self.italic = italic
        self.bold = bold
        self.underline = underline
        self.sysfont = sysfont
        self.clicked = False
        self.color = [self.normal_color, self.select_color, self.hover_color]
        self.color_number = 0
        self.get_text = text

        self.text = Text(self.get_text, self.font, self.size, font_dir=self.font_dir, color=pygame.Color(self.color[self.color_number]), italic=self.italic, bold=self.bold, underline=self.underline, sysfont=self.sysfont)
        
    def draw(self, surface, x, y):

        action = False

        self.rect = self.text.get_text_rect()
        self.rect.topleft = (x, y)

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            self.color_number = 2
            self.text = Text(self.get_text, self.font, self.size, font_dir=self.font_dir, color=pygame.Color(self.color[self.color_number]), italic=self.italic, bold=self.bold, underline=self.underline, sysfont=self.sysfont)

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                
                self.clicked = True
                
                if self.get_action == True:

                    action = True
                    # print("Click")

                else:
                    
                    self.action = UIaction(self.get_action)

            if pygame.mouse.get_pressed()[0] == 1:
                self.color_number = 1
                self.text = Text(self.get_text, self.font, self.size, font_dir=self.font_dir, color=pygame.Color(self.color[self.color_number]), italic=self.italic, bold=self.bold, underline=self.underline, sysfont=self.sysfont)

        else:
            
            self.color_number = 0
            self.text = Text(self.get_text, self.font, self.size, font_dir=self.font_dir, color=pygame.Color(self.color[self.color_number]), italic=self.italic, bold=self.bold, underline=self.underline, sysfont=self.sysfont)

        if pygame.mouse.get_pressed()[0] == 0:

            if self.clicked == True:
                self.color_number = 1
            
            self.clicked = False
        
        self.text.draw(surface, x, y)

        if self.action == True:

            return action

# En desarrollo 

# class ImageButton():
    
#     def __init__(self, image, hover_image, select_image, scale=1.0):

#         width = image.get_width()
#         height = image.get_heigth()
#         self.image = pygame.transform.scale(image, (width * scale, height * scale))
        
#         self.clicked = False

#     def draw(self, surface, x, y):
        
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)


# Aun sigo trabajando en está caracteristica, ¿Que más se puede agregar?

class UIaction():

    def __init__(self, action):

        self.action = action

        if self.action == "quit":
            self.Quit()

    def Quit(self):

        sys.exit()
        pygame.quit()