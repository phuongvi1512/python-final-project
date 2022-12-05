import pygame
import os, math
from pygame.locals import *
# class Player(pygame.sprite.Sprite):
#     def __init__(self, pos):
#         super(Player, self).__init__()
#         self.original_image = pygame.image.load("spaceship_yellow.png")
#         self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image, (55, 40)), 90)
#         self.rect = self.image.get_rect()
#         #self.sound = pygame.mixer.Sound(...)
#         self.is_active = False
#         self.is_exploded = False

#     def move(self, ):

VEL = 5

pygame.init()
	
width,height = 1000, 500
window = pygame.display.set_mode((width,height))

bg_img = pygame.image.load("images/space.png")
bg_img = pygame.transform.scale(bg_img,(width,height))

spaceship = pygame.image.load("images/spaceship_yellow.png")
spaceship = pygame.transform.rotate(pygame.transform.scale(spaceship, (55, 40)), 90)

enemy = pygame.image.load("images/spaceship_red.png")
enemy = pygame.transform.scale(enemy, (55, 40))
top_screen_enemy = pygame.transform.rotate(enemy, 180)

#event for enemy attacking
ENEMY_ATTACK = pygame.USEREVENT + 1

#event for hitting enemy
GOT_HITTED = pygame.USEREVENT + 2
ENEMY_GOT_HITTED = pygame.USEREVENT + 3

#event for crash
CRASH = pygame.USEREVENT + 4

explosion_img = pygame.image.load("images/explosion.png")
explosion_img = pygame.transform.scale(explosion_img, (100, 80))

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x < 1000 - 40:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + VEL  < 1000 - 15:  # DOWN
        yellow.y += VEL

def handle_bullets(yellow_bullets, yellow): #add direction: back, forwatd, down or up
    for bullet in yellow_bullets:
        direction = bullet[1]
        #     #if red.colliderect(bullet):
        #         #pygame.event.post(pygame.event.Event(RED_HIT))
#CODE HOW TO SHOOT
        match direction:
            case "forward":
                bullet[0].x += 7
                if bullet[0].x >= 1000: #remove bullet if x > screen width
                    yellow_bullets.remove(bullet)
            
            case "backward":
                bullet[0].x -= 7
                if bullet[0].x <= 0: #remove bullet if x < 0, out of screen
                    yellow_bullets.remove(bullet)

            case "upward":
                bullet[0].y -= 7
                if bullet[0].y  <= 0: #remove bullet if y > 0, out of screen height
                    yellow_bullets.remove(bullet)

            case "downward":
                bullet[0].y += 7 #remove bullet if y > screen height
                if bullet[0].y >= 500:
                    yellow_bullets.remove(bullet)        


#CODE ENEMY CHASING
# import math
# import pygame
# from pygame.locals import *

# class Enemy(object):
#     ...
#     def move_towards_player(self, player):
#         # Find direction vector (dx, dy) between enemy and player.
#         dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
#         dist = math.hypot(dx, dy)
#         dx, dy = dx / dist, dy / dist  # Normalize.
#         # Move along this normalized vector towards the player at current speed.
#         self.rect.x += dx * self.speed
#         self.rect.y += dy * self.speed

#     # Same thing using only pygame utilities
#     def move_towards_player2(self, player):
#         # Find direction vector (dx, dy) between enemy and player.
#         dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,
#                                       player.rect.y - self.rect.y)
#         dirvect.normalize()
#         # Move along this normalized vector towards the player at current speed.
#         dirvect.scale_to_length(self.speed)
#         self.rect.move_ip(dirvect)

#LINK FOR ENEMY CHASING
#https://stackoverflow.com/questions/20044791/how-to-make-an-enemy-follow-the-player-in-pygame

def move_towards_player(enemy, player):
    dx, dy = player.x - enemy.x, player.y - enemy.y
    dist = math.hypot(dx, dy)
    if dist != 0:
        dx, dy = dx / dist, dy / dist
        enemy.x += dx * 3 #enemy.speed
        enemy.y += dy * 3 #enemy.speed

def is_shooting_player(enemy, player):
    dx, dy = player.x - enemy.x, player.y - enemy.y
    dist = math.hypot(dx, dy)

    if dist <= 300 and dx in range(30):
        pygame.event.post(pygame.event.Event(ENEMY_ATTACK))
    if dist <= 300 and dy in range(30):
        pygame.event.post(pygame.event.Event(ENEMY_ATTACK))

def crash(enemy, player):
    dx, dy = player.x - enemy.x, player.y - enemy.y
    dist = math.hypot(dx, dy)
    if dist == 0:
        pygame.event.post(pygame.event.Event(CRASH))

def handle_enemy_bullet_direction(enemy, player):
    dx, dy = player.x - enemy.x, player.y - enemy.y
    #if player.x == enemy.x and player.y > enemy.y:
    if dx == 0 and dy > 0:
        direction = "downward"
    #elif player.x == enemy.x and player.y < enemy.y:
    elif dx == 0 and dy < 0:
        direction = "upward"
    # elif player.y == enemy.y and player.x > enemy.x:
    elif dy == 0 and dx > 0:
        direction = "forward"
    #elif player.y == enemy.y and player.x < enemy.x:
    elif dy == 0 and dx < 0:
        direction = "backward"
    else:
        return None
    return direction

#yellow spaceship space
yellow = pygame.Rect(100, 300, 55, 40)
yellow_bullets = []

#enemy spaceship
red = pygame.Rect(500, 300, 55, 40)
red_bullets = []

#another enemy
top_enemy = pygame.Rect(55, 40, 55, 40)

runing = True
while runing:
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            runing = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and len(yellow_bullets) < 3: #to shoot backward
                bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                yellow_bullets.append([bullet, "backward"])
            if event.key == pygame.K_d and len(yellow_bullets) < 3: #shoot forward
                bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                yellow_bullets.append([bullet, "forward"])
            if event.key == pygame.K_w and len(yellow_bullets) < 3: #shoot upward
                bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                yellow_bullets.append([bullet, "upward"])
            if event.key == pygame.K_s and len(yellow_bullets) < 3: #shoot downward
                bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                yellow_bullets.append([bullet, "downward"])
        
        if event.type == ENEMY_ATTACK:
            bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
            direction = handle_enemy_bullet_direction(red, yellow)
            if len(red_bullets) < 5 and direction is not None:
                red_bullets.append([bullet, direction])
                
        # if event.type == CRASH:
        #     print("crash")
        #     explosion_size = pygame.Rect(red.x, red.y, 100, 80)
        #     window.blit(explosion_img, (explosion_size.x, explosion_size.y))
        #     event.type = QUIT

    keys_pressed = pygame.key.get_pressed()
    
    yellow_handle_movement(keys_pressed, yellow)
    move_towards_player(red, yellow)
    handle_bullets(yellow_bullets, yellow)
    #handle_enemy_bullet(red, yellow, red_bullets)
    handle_bullets(red_bullets, red)
    is_shooting_player(red, yellow)
    crash(red, yellow)
    
    #pygame.time.Clock().tick(30)
    window.blit(bg_img,(0,0))
    window.blit(spaceship, (yellow.x, yellow.y))

    #add enemy image
    window.blit(top_screen_enemy, (top_enemy.x, top_enemy.y))
    window.blit(enemy, (red.x, red.y))
    
    for bullet in yellow_bullets:
        pygame.draw.rect(window, (255, 255, 0), bullet[0])

    for bullet in red_bullets:
        pygame.draw.rect(window, (255, 0, 0), bullet[0])

    pygame.display.update()
pygame.quit()


# WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
# keys_pressed = pygame.key.get_pressed()
#         yellow_handle_movement(keys_pressed, yellow)



