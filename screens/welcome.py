import pygame
from .base import BaseScreen
from text import TextBox
from globalvars import *
#from ..components import Background, Logo

bg_img = pygame.image.load("images/space.png")
bg_img = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))
class WelcomeScreen(BaseScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #Put back default screen size
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        
        
        # #Main Background Class
        # self.background = Background()

        # #League logo
        # self.league_logo = Logo("./images/leaguelogo.png", (350, 150), [235, 100])
        
        #Sprite Groupe
        self.sprites = pygame.sprite.Group()

        #Instruction textbox
        self.textbox2 = TextBox(
            (200, 100), "Let's play", color=(255, 255, 255), bgcolor=(0, 0, 255)
        )
        self.textbox2.rect.x, self.textbox2.rect.y= 50, 400

        #How to start Textbox
        self.textbox3 = TextBox(
            (200, 100), "Annie", color=(255, 255, 255), bgcolor=(255, 0, 0)
        )
        self.textbox3.rect.x, self.textbox3.rect.y= 300, 400

        self.sprites.add(self.textbox2, self.textbox3)

    def draw(self):
        self.window.fill((255, 255, 255))
        self.window.blit(bg_img,(0,0))
        # self.window.blit(self.background.image, self.background.rect)
        # self.window.blit(self.league_logo.image, self.league_logo.rect)
        self.sprites.draw(self.window)

    def update(self):
        pass

    def manage_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = event.pos
            if self.textbox2.rect.collidepoint(mouse):
                self.next_screen = "game"
                self.running = False