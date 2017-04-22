#!/usr/bin/python
# -*- coding: utf-8 -*-

# Main.py

import os
import random

import pygame as pg


class Constants:
    FPS = 60
    NAVY = (0, 0, 128)
    money_array = []
    MONEY_SIZE = 70

# Constructor for constants file for many variables

constants = Constants()

class Game(object):

    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.game_over = False
        self.wallet_x = 0
        self.wallet_y = 0
        self.wallet_x_movement = 0
        self.wallet_y_movement = 1

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()
        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        self.wallet_x += self.wallet_x_movement
        self.wallet_y += self.wallet_y_movement

    def display_frame(self, screen):
        if self.game_over:
            font = pg.font.SysFont('serif', 25)
            text = font.render('Game Over, click to restart', True,
                               BLACK)
            center_x = SCREEN_WIDTH // 2 - text.get_width() // 2
            center_y = SCREEN_HEIGHT // 2 - text.get_height() // 2
            screen.blit(text, [center_x, center_y])



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

def main():
    """ Main statement for initialize of program, also controller for executing.
    """
    pg.init()
    done = paused = False
    clock = pg.time.Clock()
    display_info = pg.display.Info()

    display_surface = pg.display.set_mode((750, 550))

    game = Game()
    images = load_images()

    while not done:
        done = game.process_events()
        game.run_logic()
        display_surface.fill(pg.Color("white"))
        game.display_frame(display_surface)
        display_surface.blit(images['wallet'], (game.wallet_x, game.wallet_y))
        pg.display.update()
        clock.tick(constants.FPS)
    pg.quit()


if __name__ == '__main__':
    main()
