import pygame
from settings import Settings


class Builder(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("images/builder0.png")
        self.anim_right = [pygame.image.load("images/builder_1.png"), pygame.image.load("images/builder_2.png")]
        self.anim_left = [pygame.image.load("images/builder1.png"), pygame.image.load("images/builder2.png")]
        self.rect = self.image.get_rect()
        self.rect.top = Settings().builder_top
        self.rect.left = Settings().builder_left
        self.ticks = 0
        self.anim_queue = []
        self.ready = False

    def play_anim(self):
        if len(self.anim_queue) == 0:
            return
        self.ready = False
        if self.ticks == 4:
            if self.anim_queue[0] == "to_right" or self.anim_queue[0] == "from_right":
                self.image = self.anim_right[0]
            if self.anim_queue[0] == "to_left" or self.anim_queue[0] == "from_left":
                self.image = self.anim_left[0]
        if self.ticks == 8:
            if self.anim_queue[0] == "to_right":
                self.image = self.anim_right[1]
            if self.anim_queue[0] == "to_left":
                self.image = self.anim_left[1]
            if self.anim_queue[0] == "from_right" or self.anim_queue[0] == "from_left":
                self.image = pygame.image.load("images/builder0.png")
            self.ticks = 0
            self.anim_queue.pop(0)
        self.ticks += 1

    def reset(self):
        self.image = pygame.image.load("images/builder0.png")

    def update(self):
        self.play_anim()

    def blitme(self):
        self.screen.blit(self.image, self.rect)
