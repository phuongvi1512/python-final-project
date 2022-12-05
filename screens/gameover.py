import pygame, requests
from .base import BaseScreen
from text import TextBox, InputBox
#import webbrowser


class GameOverScreen(BaseScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Check if username is submitted
        self.submit = False

        #Sprites
        self.sprites = pygame.sprite.Group()
        self.button1 = TextBox(
            (100, 100), "Again", color=(0, 255, 0), bgcolor=(255, 255, 255)
        )
        self.button2 = TextBox(
            (100, 100), "Quit", color=(255, 0, 0), bgcolor=(255, 255, 255)
        )
        #HOW TO ADD TIME HERE
        self.button3 = TextBox(
            (400, 100), f'SCORE = {self.state["score"]}', color=(255, 255, 255), bgcolor=(0, 0, 0)
        )
        self.button4 = TextBox(
            (400, 100), f'Survived = {int(self.state["time_alive"])}s', color=(255, 255, 255), bgcolor=(0, 0, 0)
        )

        #If you are only show the leaderboard link
        if self.state["online"] == True:
            self.button7 = TextBox(
                (400, 200), 'VIEW LEADERBOARD', color=(0, 0, 0), bgcolor=(255, 255, 255)
            )
            self.button7.rect.topleft = (200, 500)
            self.sprites.add(self.button7)

        self.button1.rect.topleft = (200, 100)
        self.button2.rect.topleft = (500, 100)
        self.button3.rect.topleft = (200, 300)
        self.button4.rect.topleft = (200, 400)
        self.sprites.add(self.button1, self.button2, self.button3, self.button4)


    
    def update(self):
        if self.submit == False and self.state["online"] == True:
            requests.post(f"http://127.0.0.1:5000/addscore/{self.state['username']}", json=self.state)
            self.submit = True

    def draw(self):
        self.window.fill((255, 255, 255))
        self.sprites.draw(self.window)
        

    def manage_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button1.rect.collidepoint(event.pos):
                self.running = False
                self.next_screen = "welcome"
            elif self.button2.rect.collidepoint(event.pos):
                self.running = False
                self.next_screen = False
            if self.state["online"] == True:
                if self.button7.rect.collidepoint(event.pos):
                    webbrowser.open_new('http://127.0.0.1:5000/leaderboard')
