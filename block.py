import pygame
import time
from glob import GlobalState
from settings import Settings
import random


class Block(pygame.sprite.Sprite):

    def __init__(self, bracing):
        super().__init__()
        self.screen = bracing.screen
        self.image = pygame.image.load("images/block.jpg")
        self.trans = pygame.image.load("images/transparent.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = bracing.center
        self.rect.top = GlobalState().y0
        self.release_time = time.time()
        self.stop = False
        self.state = 'default'
        self.dir_set = 'none'

    def update(self, bracing):
        if GlobalState().over:
            self.rect.centerx = -100
            return
        if self.state == 'default':
            if not self.stop:
                current_time = time.time()
                t = current_time - self.release_time
                self.rect.top = GlobalState().y0 + GlobalState().acceleration * t ** 2
                if self.dir_set == 'none':
                    if bracing.moving_right:
                        self.dir_set = 'right'
                    elif bracing.moving_left:
                        self.dir_set = 'left'
                    else:
                        self.dir_set = 'center'
                if self.dir_set == 'right':
                    self.rect.centerx += GlobalState().bracing_speed - 2
                elif self.dir_set == 'left':
                    self.rect.centerx -= GlobalState().bracing_speed - 2
        elif self.state == 'static':
            width = self.rect.right - self.rect.left
            interval = True if random.random() > 0.5 else False
            left_edge = 10
            right_edge = Settings().screen_width - 350
            left = bracing.rect.centerx - int(width * 1.5)
            right = bracing.rect.centerx + int(width * 0.5)
            if left < left_edge:
                self.rect.left = random.randint(right, right_edge)
            elif right > right_edge:
                self.rect.left = random.randint(left_edge, left)
            else:
                if interval:
                    self.rect.left = random.randint(left_edge, left)
                else:
                    self.rect.left = random.randint(right, right_edge)
            self.state = 'waiting'
        elif self.state == 'waiting':
            GlobalState().blocked = True
            if abs(bracing.rect.centerx - self.rect.centerx) < 5:
                self.state = 'hooked'
        elif self.state == 'hooked':
            GlobalState().blocked = False
            self.rect.centerx = bracing.rect.centerx

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def make_static(self):
        self.state = 'static'
