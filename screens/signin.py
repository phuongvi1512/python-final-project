import pygame
from screens import BaseScreen
from text import InputBox, TextBox
from text import render_text
#from text import render_text
from globalvars import *
#from ..components import Background
import requests

bg_img = pygame.image.load("images/welcom.png")
bg_img = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))

class Login(BaseScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window = pygame.display.set_mode((736, 476))

        #Background
        #self.background = Background('./images/welcom.png')

        #Check if username is submitted
        self.invalid = False
        self.invalid_user = ''

        #Buttons 
        self.sprites = pygame.sprite.Group()

        self.button1 = TextBox(
            (100, 50), "Quit", color=(255, 255, 255), bgcolor=(255,0,0)
        )
        self.button2 = TextBox(
            (100, 50), "Login", color=(0, 0, 0), bgcolor=(249,232,176)
        )
        self.button3 = TextBox(
            (200, 50), "Play Offline", color=(255, 255, 255), bgcolor=(0, 0, 0)
        )
        self.button1.rect.topleft = (638, 425)
        self.button2.rect.topleft = (400, 325)
        self.button3.rect.topleft = (0, 425)
        self.sprites.add(self.button1, self.button2, self.button3)

        #Text
        self.text1 = render_text('Username', 20)
        self.text3 = render_text('Login with Username to Play', 28)
        self.text4 = render_text('Password', 20)

        #TextBox 
        self.input_box = InputBox(280, 170, 600, 50, '')
        self.input_password = InputBox(280, 270, 600, 50, '')

    
    def update(self):
        self.input_box.update()
        self.input_password.update()
        self.get_user()
        self.button4 = TextBox(
            (250, 50), f'"{self.invalid_user}" ALREADY EXISTS',text_size = 18, color=(255, 0, 0), bgcolor=(249,232,176)
        )
        self.button4.rect.topleft = (150, 325)

    def draw(self):
        self.window.fill((255, 255, 255))
        self.window.blit(bg_img,(0,0))
        self.sprites.draw(self.window)
        self.window.blit(self.text1, (140, 184))
        self.window.blit(self.text3, (175, 100))
        self.window.blit(self.text4, (140, 284))
        self.input_box.draw(self.window)
        self.input_password.draw(self.window)
        if self.invalid == True:
            self.sprites.add(self.button4)
        

    def manage_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button1.rect.collidepoint(event.pos):
                self.running = False
                self.next_screen = False
                
            #Click Login
            if self.button2.rect.collidepoint(event.pos):
                    self.input_box.entered = self.input_box.text
                    self.input_password.entered = self.input_password.text
            
            #If click play offline play without having to login
            if self.button3.rect.collidepoint(event.pos):
                self.state["online"] = False
                self.running = False
                self.next_screen = 'welcome'


        #Manage input box event
        self.input_box.handle_event(event)
        self.input_password.handle_event(event)
    def get_user(self):
        if self.input_box.entered != '' and self.input_password.entered != '':
            username = self.input_box.entered
            password = self.input_password.entered
            data = {"username": username, "password": password}
            x = requests.post(f"http://127.0.0.1:5000/register", json=data)
            valid_user = x.status_code
            print(valid_user)

            if valid_user == 200:
                self.state["username"] = username
                self.state["password"] = password
                self.state["online"] = True
                self.next_screen = 'welcome'
                self.running = False
            elif valid_user == 404:
                self.invalid_user = username
                self.invalid = True