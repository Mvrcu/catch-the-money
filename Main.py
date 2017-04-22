#!/usr/bin/python
# -*- coding: utf-8 -*-

# Main.py

import os
import sys
import random

import pygame as pg


CAPTION = "Catch the falling funds with your wallet!"
SCREEN_SIZE = (800, 550)

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


class Money(pg.sprite.Sprite):
    def __init__(self, screen_rect, *groups):
        """
        The pos argument is a tuple for the center of the player (x,y);
        speed is given in pixels/frame.
        """
        super(Money, self).__init__(*groups)
        self.image = IMAGES["money"]
        self.rect = self.image.get_rect()
        self.reset(screen_rect)

    def reset(self, screen_rect):
        self.speed = random.randrange(1, 5)
        self.rect.y = random.randrange(-300, -self.rect.h)
        self.rect.x = random.randrange(0, screen_rect.w - self.rect.w)

    def update(self, screen_rect, *args):
        self.rect.y += self.speed
        if self.rect.top > screen_rect.h:
            self.reset(screen_rect)


class Player(pg.sprite.Sprite):
    """
    This class will represent our user controlled character.
    """

    def __init__(self, pos, speed, *groups):
        """
        The pos argument is a tuple for the center of the player (x,y);
        speed is given in pixels/frame.
        """
        super(Player, self).__init__(*groups)
        self.image = IMAGES["wallet"]
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.score = 0

    def update(self, screen_rect, keys):
        """
        Updates our player appropriately every frame.
        """
        for key in DIRECT_DICT:
            if keys[key]:
                self.rect.x += DIRECT_DICT[key][0]*self.speed
                self.rect.y += DIRECT_DICT[key][1]*self.speed
        self.rect.clamp_ip(screen_rect)


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
        self.allsprites = pg.sprite.Group()
        self.object_sprites = pg.sprite.Group()
        self.player = Player(self.screen_rect.center, 5, self.allsprites)
        for _ in range(15):
            Money(self.screen_rect, self.allsprites, self.object_sprites)

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
        self.allsprites.draw(self.screen)
        pg.display.update()

    def update(self):
        hit_list = pg.sprite.spritecollide(self.player, self.object_sprites, True)
        for i in hit_list:
            self.player.score += 1
            print(self.player.score)
        self.allsprites.update(self.screen_rect, self.keys)

    def update_score(self):
        font = pg.font.SysFont('Calibri', 25, True, False)
        text = font.render("Score: "+ str(self.player.score), True, pg.Color("black"))
        self.screen.blit(text, [5, 5])

    def main_loop(self):
        """
        One game loop. Simple and clean.
        """
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.update_score()
            self.clock.tick(self.fps)

def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    global IMAGES
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE, pg.NOFRAME)
    IMAGES = load_images()
    Application().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
