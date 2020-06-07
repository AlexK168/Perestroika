import pygame
import peewee
from peewee import *
from settings import Settings
from bracing import Bracing
from block import Block
import game_functions as gf
from pygame.sprite import Group
from glob import GlobalState
from tower import Tower
from builder import Builder
from button import Button

db = MySQLDatabase(database='perestroika', user='root', passwd='')


class Record(peewee.Model):
    user = peewee.CharField()
    score = peewee.IntegerField()

    class Meta:
        database = db


def run_game():
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.mixer.music.load('sounds/bg_music.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.4)
    pygame.display.set_caption("Perestroika")

    bracing = Bracing(screen)
    GlobalState(bracing)
    blocks = Group()
    tower = Tower()
    trucks = Group()
    record = None
    for r in Record.filter(user="user"):
        record = r
    if record is None:
        record = Record(user="user", score=0)
    record.save()

    builder = Builder(screen)
    block = Block(bracing)
    block.make_static()
    button = Button(screen)
    while True:
        var = gf.check_events(bracing, blocks, tower, builder, block, trucks, button)
        if var is not None and var > record.score:
            record.score = var
            print(var)
            record.save()
        builder.update()
        bracing.update()
        blocks.update(bracing)
        block.update(bracing)
        trucks.update()
        gf.update_screen(screen, bracing, blocks, builder, block, trucks, button)
        GlobalState().ticks += 1


run_game()
