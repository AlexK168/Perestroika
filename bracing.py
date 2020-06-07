import pygame
from settings import Settings
from glob import GlobalState


class Bracing(pygame.sprite.Sprite):

    def __init__(self, screen):

        super().__init__()
        self.screen = screen

        self.image = pygame.image.load("images/bracing.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.top + 170
        self.moving_right = False
        self.moving_left = False
        self.center = float(self.rect.centerx)
        self.shaker = 1

    def update(self):
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= GlobalState().bracing_speed
        if self.moving_right and self.rect.right < self.screen_rect.right - 200:
            self.center += GlobalState().bracing_speed
        self.rect.centerx = self.center
        if self.moving_left or self.moving_right:
            self.shaker *= -1
            self.rect.top += self.shaker
        else:
            self.rect.top = self.screen_rect.top + 170

    def blitme(self):
        self.screen.blit(self.image, self.rect)
