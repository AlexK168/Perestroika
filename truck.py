import pygame
from settings import Settings
import random


class Truck(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.moving_right = False
        self.shaker = 1
        self.speed = 4
        image = "images/truck"
        image += str(random.randint(0, 2)) + '_'
        if random.randint(0, 1) == 0:
            self.moving_right = True
            image += 'r'
        else:
            self.moving_right = False
            image += 'l'
        image += '.png'
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        if self.moving_right is True:
            self.rect.right = 0
            self.rect.bottom = Settings().road_right_line
        else:
            self.rect.left = Settings().screen_width
            self.rect.bottom = Settings().road_left_line

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if (self.moving_right and self.rect.left >= Settings().screen_width) or (not self.moving_right and self.rect.right <= 0):
            self.kill()
            return
        if self.moving_right:
            self.rect.left += self.speed
        else:
            self.rect.left -= self.speed
        self.shaker *= -1
        self.rect.top += self.shaker
