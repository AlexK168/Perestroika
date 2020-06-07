import pygame


class Button:

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load("images/butt.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.bottom = 450

    def draw_button(self):
        self.screen.blit(self.image, self.rect)
