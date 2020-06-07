import pygame
from singleton import Singleton


class Settings(metaclass=Singleton):

    def __init__(self):
        self.screen_width = 1180
        self.screen_height = 1000
        self.bg_color = (255, 255, 255)
        self.bg_pic = pygame.image.load("images/bg.jpg")
        self.builder_top = 152
        self.builder_left = 1002
        self.road_left_line = 840
        self.road_right_line = 870
        self.car_speed = 3

