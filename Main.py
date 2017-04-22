#!/usr/bin/python
# -*- coding: utf-8 -*-

# Main.py

import os
import random
import sys

import pygame as pg


CAPTION = "Move me with the Arrow Keys"
SCREEN_SIZE = (700, 500)

TRANSPARENT = (0, 0, 0, 0)

# This global constant serves as a very useful convenience for me.
DIRECT_DICT = {pg.K_LEFT  : (-1, 0),
               pg.K_RIGHT : ( 1, 0),
               pg.K_UP    : ( 0,-1),
               pg.K_DOWN  : ( 0, 1)}

def load_images():
    """Loads all images in 'img' folder for use on call."""

    def load_image(img_file):
        """
        This function gathers all relevant images in the image folder of the
        game.
        """
        directory = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(directory, 'img', img_file)
        return pg.image.load(file_name).convert_alpha()

    return {'money': load_image('money.png'),
            'wallet': load_image('wallet.png'),
            'bonus_card': load_image('bonus_card.png'),
            'saw': load_image('saw.png')}

class Player(object):
    """
    This class will represent our user controlled character.
    """
    SIZE = (100, 100)

    def __init__(self, pos, speed):
        """
        The pos argument is a tuple for the center of the player (x,y);
        speed is given in pixels/frame.
        """
        self.rect = pg.Rect((0,0), Player.SIZE)
        self.rect.center = pos
        self.speed = speed
        self.image = load_images()

    def update(self, keys, screen_rect):
        """
        Updates our player appropriately every frame.
        """
        for key in DIRECT_DICT:
            if keys[key]:
                self.rect.x += DIRECT_DICT[key][0]*self.speed
                self.rect.y += DIRECT_DICT[key][1]*self.speed
        self.rect.clamp_ip(screen_rect) # Keep player on screen.

    def draw(self, surface):
        """
        Blit image to the target surface.
        """
        surface.blit(self.image['wallet'], self.rect)


class Application(object):
    """
    A class to manage our event, game loop, and overall program flow.
    """
    def __init__(self):
        """
        Get a reference to the display surface; set up required attributes;
        and create a Player instance.
        """
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.keys = pg.key.get_pressed()
        self.player = Player(self.screen_rect.center, 5)

    def event_loop(self):
        """
        One event loop. Never cut your game off from the event loop.
        Your OS may decide your program has hung if the event queue is not
        accessed for a prolonged period of time.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type in (pg.KEYUP, pg.KEYDOWN):
                self.keys = pg.key.get_pressed()

    def render(self):
        """
        Perform all necessary drawing and update the screen.
        """
        self.screen.fill(pg.Color("white"))
        self.player.draw(self.screen)
        pg.display.update()

    def main_loop(self):
        """
        One game loop. Simple and clean.
        """
        while not self.done:
            self.event_loop()
            self.player.update(self.keys, self.screen_rect)
            self.render()
            self.clock.tick(self.fps)

def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE, pg.NOFRAME)
    Application().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
