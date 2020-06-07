import sys

import pygame
import peewee
from peewee import *

from settings import Settings
from block import Block
from glob import GlobalState
from truck import Truck



def check_keydown_events(event, bracing, blocks, tower, builder, block):
    if event.key == pygame.K_RIGHT and not GlobalState().over:
        bracing.moving_right = True
        builder.anim_queue.append("to_right")
        builder.right = True
    elif event.key == pygame.K_LEFT and not GlobalState().over:
        bracing.moving_left = True
        builder.anim_queue.append("to_left")
        builder.left = True
    elif event.key == pygame.K_SPACE and not GlobalState().blocked and not GlobalState().falling:
        new_block = Block(bracing)
        blocks.add(new_block)
        tower.push(new_block)
        GlobalState().falling = True
        block.state = 'static'
        GlobalState().played = False
    elif event.key == pygame.K_p:
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_CTRL:
            GlobalState().score += 50


def check_keyup_events(event, bracing, builder):
    if event.key == pygame.K_RIGHT and not GlobalState().over:
        bracing.moving_right = False
        builder.right = False
        builder.anim_queue.append("from_right")
    elif event.key == pygame.K_LEFT and not GlobalState().over:
        bracing.moving_left = False
        builder.left = False
        builder.anim_queue.append("from_left")


def check_collisions(blocks):
    sprite_list = blocks.sprites()
    inv_sprite_list = sprite_list
    if len(sprite_list) == 0:
        return
    if len(sprite_list) == 1:
        if sprite_list[0].rect.bottom >= Settings().screen_height:
            sprite_list[0].stop = True
            sprite_list[0].rect.bottom = Settings().screen_height
            GlobalState().falling = False
    else:
        top_block = sprite_list[-1]
        width = top_block.rect.right - top_block.rect.left
        pre_top_block = sprite_list[-2]
        offset = abs(top_block.rect.left - pre_top_block.rect.left)
        inv_sprite_list.reverse()
        for i in range(1, len(sprite_list)):
            new_off = abs(inv_sprite_list[i].rect.left - top_block.rect.left)
            if new_off < width:
                offset = new_off
                pre_top_block = inv_sprite_list[i]
                break
        if offset > width:
            if top_block.rect.bottom >= Settings().screen_height:
                top_block.stop = True
                top_block.rect.bottom = Settings().screen_height
                GlobalState().falling = False
        elif top_block.rect.bottom >= pre_top_block.rect.top:
            top_block.stop = True
            top_block.rect.bottom = pre_top_block.rect.top
            GlobalState().falling = False


def check_game(bracing, blocks, tower, builder, block):
    if GlobalState().over and not GlobalState().falling:  # resetting
        bracing.moving_left = False
        bracing.moving_right = False
        builder.reset()
        for i in range(tower.size):
            tower.pop()
            blocks.remove(blocks.sprites()[0])
        GlobalState().blocked = False
        GlobalState().falling = False
        block.make_static()
        score = GlobalState().score
        GlobalState().score = 0
        return score

    return None


def normalize_tower(blocks):
    height = blocks.sprites()[0].rect.top - blocks.sprites()[0].rect.bottom
    for b in blocks:
        b.rect.top -= height


def check_limit(blocks, tower):
    if len(tower) >= GlobalState().limit:
        if blocks.sprites()[-1].stop:
            for i in range(1):
                tower.pop()
                blocks.remove(blocks.sprites()[0])
            normalize_tower(blocks)


def spawn_trucks(trucks, screen):
    if GlobalState().ticks >= 400:
        trucks.add(Truck(screen))
        GlobalState().ticks = 0


def check_start_button(button, mouse_x, mouse_y):
    if button.rect.collidepoint(mouse_x, mouse_y) and GlobalState().over:
        GlobalState().over = False


def check_events(bracing, blocks, tower, builder, block, trucks, button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, bracing, blocks, tower, builder, block)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, bracing, builder)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_start_button(button, mouse_x, mouse_y)
    spawn_trucks(trucks, bracing.screen)
    check_collisions(blocks)
    check_limit(blocks, tower)
    if not tower.sustainable:
        GlobalState().blocked = True
        GlobalState().over = True
    check_limit(blocks, tower)
    var = check_game(bracing, blocks, tower, builder, block)
    return var


def update_screen(screen, bracing, blocks, builder, block, trucks, button):
    screen.blit(Settings().bg_pic, (0, 0))
    trucks.draw(screen)
    blocks.draw(screen)
    bracing.blitme()
    builder.blitme()

    block.blitme()
    if GlobalState().over:
        button.draw_button()
    pygame.display.flip()
