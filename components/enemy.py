import pygame
from pygame.locals import *
from .spaceship import Spaceship
from .player import Player
from __init__ import *
import random, math
from ..globalvars import *
from bullet import EnemyBullet


#image of enemy spaceship
enemy_img = pygame.image.load("images/spaceship_red.png")

class Enemy(Spaceship):
    """
    enemy class is a children class of spaceship
    enemy class is created in posx, posy (it will be based on in gamescreen)
    when distance between enemy and player is within a certain range, the enemy can shoot player
    if player and enemy in the same vertical or horizontal line, the enemy start attacking 
    the shooting direction can be forward, backward, upward, downward along with the screen

    """
    def __init__(self, posx, posy):
        super.__init__(enemy_img, posx, posy, )
        self.rect = self.image.get_rect()
        
        # #starting position
        # self.rect.x = 500  
        # self.rect.y = 300

        self.speed = ENEMY_ORIGINAL_SPEED
        self.range_to_shoot = RANGE_TO_SHOOT

        self.is_exploded = False
        self.bullets = []

    def draw(self, window):
        pass

    def get_distance(self, player: Player):
        """
        find distance between player and enemy using math.hypot
        find vertical and horizontal vector (x, y) between player and enemy 
        """
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        return dx, dy, dist 
        

    def move_towards_player(self, player: Player):
        dx, dy, distance = self.get_distance(player)
        if distance != 0:
            dx, dy = dx / distance, dy / distance
            self.rect.x += dx * self.speed 
            self.rect.y += dy * self.speed

    def get_shooting_direction(self, player: Player):
        dx, dy, distance = self.get_distance(player)
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

    def shoot(self, player: Player):
        """
        check if distance between player and enemy is in certain range
        create bullets and shoot the player based on direction of bullet
        """
        dx, dy, distance = self.get_distance(player)
        direction = self.get_shooting_direction(player)
        if distance <= self.range_to_shoot and direction is not None:
            bullet = EnemyBullet(direction, self.rect.x, self.rect.y)
            bullet.draw()
            bullet.update()

    def update_enemy(self, player: Player):
        """
        update position of enemy and check if can shoot player
        """
        # self.update()
        self.move_towards_player(player)
        self.shoot(player)

