import pygame
from pygame.locals import *
from globalvars import * #import colors for enemy and player bullets
class Bullet(pygame.sprite.Sprite):
    """
    class Bullet
    bullet can be shot to 4 different directions along with screen: Upward, Backward, Forward (Right on screen), Backward(left on screen)
    bullet can have different color
    bullet is a small rectangle showed on screen
    """
    def __init__(self, color, direction: str, posx, posy):
        super().__init__()
        self.color = color
        #self.pos = pos
        self.direction = direction
        #self.image = pygame.Surface((10, 5))
        #self.image.fill(self.color)
        #self.rect = self.image.get_rect()

        #position of bullet
        #bullet position will depend on position of player or enemy
        self.posx = posx
        self.posy = posy
        self.speed = 7
    
    def draw(self, window):
        #window.blit(self.image, self.rect)
        #pygame.draw.rect(window, (255, 0, 0), bullet[0])
        #bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
        """

        """
        bullet = pygame.Rect(self.posx, self.posy//2 -2, 10, 5)
        pygame.draw.rect(window, self.color, bullet)

    def move(self):
        """
        update bullet location on screen
        how bullet moves along different directions
        if bullet goes out screen, delete the bullet
        """
        if self.direction == "forward":
            self.posx += self.speed
        elif self.direction == "backward":
            self.posx -= self.speed
        elif self.direction == "upward":
            self.posy -= self.speed
        elif self.direction == "downward":
            self.posy += self.speed
        else:
            pass

        # Delete bullets that go off screen
        if self.posx not in range(WIDTH) or self.posy not in range(HEIGHT):
            self.kill()

    def hit_target(self, target):
        """
        function to check if the bullet hits the target
        return Boolean: true or false
        if bullet hits, remove the bullet
        """
        if pygame.sprite.spritecollide(self, target, dokill=True):
            self.kill
            return True

    def update(self):
        self.move()
        self.hit_target()
        
    
class EnemyBullet(Bullet):
    """
    enemy bullet color is Red
    """
    def __init__(self, direction, posx, posy):
        super().__init__(RED,posx, posy)



class PlayerBullet(Bullet):
    """
    player bullet color is yellow
    """
    def __init__(self, direction, posx, posy):
        super().__init__(YELLOW, direction, posx, posy)
