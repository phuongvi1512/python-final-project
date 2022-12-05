import pygame
from pygame.locals import *
from .bullet import PlayerBullet
from ..globalvars import *
from .spaceship import Spaceship
#player image is yellow spaceship
player_img = pygame.image.load("images/spaceship_yellow.png")

class Player(Spaceship):
    def __init__(self):
        """
        class Player
        children class of spaceship
        player is yellow spaceship with size (55,40)
        starting position of player is (100, 300) on screen
        player can shoot when key "a, d, w, s" get pressed
        player can move when arrow key get pressed, speed of move is 7 or defined by global variable SPEED
        player has bullets (bullets is a list to store all bullets)
        player's original health is 10, if player get hitted by enemy bullet, the health is deducted
        if health < 0, the player is dead, the ship is exploded
        """
        super.__init__(player_img, 100, 300, SPEED)
        self.is_exploded = False
        self.score = 0
        self.health = 10
      

    def get_shooting_direction(self, keys_pressed):
        if keys_pressed[pygame.K_a] and len(self.bullets) < 3:  # LEFT
            direction = "backward"
        elif keys_pressed[pygame.K_d] and len(self.bullets) < 3:  # RIGHT
            direction = "forward"
        elif keys_pressed[pygame.K_w] and len(self.bullets) < 3:  # UP
            direction = "upward"
        elif keys_pressed[pygame.K_s] and len(self.bullets) < 3:  # DOWN
            direction = "downward"
        else:
            return None
        return direction

    def add_bullet(self, keys_pressed):
        direction = self.get_shooting_direction(keys_pressed)
        bullet = PlayerBullet(YELLOW, direction, self.rect.x, self.rect.y)
        if isinstance(bullet, PlayerBullet):
            self.bullets.append(bullet)

    def remove_bullet(self, bullet: PlayerBullet):
        if len(self.bullets) > 0:
            for bullet in self.bullets.copy():
                if bullet.posx not in range(WIDTH) or bullet.posy not in range(HEIGHT):
                    self.bullets.remove(bullet)

    def shoot(self):
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.draw()
                bullet.update()

    def update_score(self):
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                if bullet.hit_target() is True:
                    self.score += 1


    def update_health(self, get_hit= False):
        if get_hit is True:
            self.health -= 1

    def get_moving_direction(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.rect.x - self.speedx > 0:  # LEFT
            direction = "backward"
        elif keys_pressed[pygame.K_RIGHT] and self.rect.x + self.speedx < 1000 - 40:  # RIGHT
            direction = "forward"
        elif keys_pressed[pygame.K_UP] and self.rect.y - self.speedx > 0:  # UP
            direction = "upward"
        elif keys_pressed[pygame.K_DOWN] and self.rect.y + self.speedx  < 1000 - 15:  # DOWN
            direction = "downward"
        else:
            return None
        return direction

    def update(self, event):
        direction = self.get_moving_direction(event)
        if direction is not None:
            self.move(direction)

        self.add_bullet(event)
        self.remove_bullet(event)
        self.shoot()
        self.update_score(event)
        self.update_health(event)
        
        if self.health == 0:
            self.is_exploded = True
