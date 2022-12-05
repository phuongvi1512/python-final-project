import pygame
from pygame.locals import *
from .bullet import Bullet
from globalvars import *

#image when spaceship is exploded
explosion = pygame.image.load("images/explosion.png")

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, image, posx, posy, speed=SPEED):
        """
        class Spaceship
        parent class of player and enemy
        spaceship can move backward, upward, downward and forward
        spaceship can shoot enemy
        spaceship can be exploded when get hit or crash
        spaceship has speed 
        original speed is imported from globalvars
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (55, 40))
        self.rect = self.image.get_rect()
        
        #starting position
        self.rect.x = posx
        self.rect.y = posy

        self.speed = speed
        self.bullets = []
        self.is_exploded = False

    def add_bullet(self, *bullets):
        # direction = self.shooting_direction(keys_pressed)
        # bullet = PlayerBullet(YELLOW, direction, self.rect.x, self.rect.y)
        # if isinstance(bullet, PlayerBullet):
        #     self.bullets.append(bullet)
        for bullet in bullets:
            if isinstance(bullet, Bullet):
                self.bullets.append(bullet)

    # def remove_bullet(self, bullet: PlayerBullet):
    #     if len(self.bullets) > 0:
    #         for bullet in self.bullets.copy():
    #             if bullet.posx not in range(WIDTH) or bullet.posy not in range(HEIGHT):
    #                 self.bullets.remove(bullet)

    def shoot(self):
        for bullet in self.bullets:
            bullet.draw()
            bullet.update()


    def move(self, direction):
        if direction == "backward" and self.rect.x - self.speed > 0:  # LEFT
            self.rect.x -= self.speed
        elif direction == "forward" and self.rect.x + self.speed < 1000 - 40:  # RIGHT
            self.rect.x += self.speed
        elif direction == "upward" and self.rect.y - self.speed > 0:  # UP
            self.rect.y -= self.speed
        elif direction == "downward" and self.rect.y + self.speed  < 1000 - 15:  # DOWN
            self.rect.y += self.speed

    def get_hit(self):
        """
        either enemy and player can be hit
        depends on the children classes
        """
        pass

    def hit_target(self, target):
        """method for player
        when the player hit enemy, player gain 1 score
        """
        pass

    def get_exploded(self):
        """
        if the spaceshipt is exploded, show image of explosion
        then kill the spaceship
        """
        if self.is_exploded is True:
            self.image = pygame.transform.scale(explosion, (55, 40))
            self.kill()

    def update(self, event):
        self.move(event)
        self.add_bullet(event)
        self.shoot()
        self.get_hit()
        self.hit_target()
        self.get_exploded()