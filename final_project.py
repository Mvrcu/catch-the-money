#!/usr/bin/python
# -*- coding: utf-8 -*-

# Main.py

import os
import sys
import random

import pygame as pg


CAPTION = "Catch the falling funds with your wallet!"
SCREEN_SIZE = (850, 600)

TRANSPARENT = (0, 0, 0, 0)

# This global constant serves as a very useful convenience for me.
DIRECT_DICT = {pg.K_LEFT  : (-2, 0),
               pg.K_RIGHT : ( 2, 0),
               pg.K_UP    : ( 0,-2),
               pg.K_DOWN  : ( 0, 2)}


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
        self.speed = random.randrange(3, 4)
        self.rect.y = random.randrange(-300, -self.rect.h)
        self.rect.x = random.randrange(0, screen_rect.w - self.rect.w)

    def update(self, screen_rect, *args):
        self.rect.y += self.speed
        if self.rect.top > screen_rect.h:
            self.reset(screen_rect)

class Saw(pg.sprite.Sprite):
    def __init__(self, screen_rect, *groups):
        """
        The pos argument is a tuple for the center of the player (x,y);
        speed is given in pixels/frame.
        """
        super(Saw, self).__init__(*groups)
        self.image = IMAGES["saw"]
        self.rect = self.image.get_rect()
        self.reset(screen_rect)

    def reset(self, screen_rect):
        self.speed = random.randrange(2, 4)
        self.rect.y = random.randrange(-300, -self.rect.h)
        self.rect.x = random.randrange(0, screen_rect.w - self.rect.w)

    def update(self, screen_rect, *args):
        self.rect.y += self.speed
        if self.rect.top > screen_rect.h:
            self.reset(screen_rect)


class Bonus_Card(pg.sprite.Sprite):
    def __init__(self, screen_rect, *groups):
        """
        The pos argument is a tuple for the center of the bonus card (x,y);
        speed is given in pixels/frame.
        """
        super(Bonus_Card, self).__init__(*groups)
        self.image = IMAGES["bonus_card"]
        self.rect = self.image.get_rect()
        self.reset(screen_rect)

    def reset(self, screen_rect):
        self.speed = random.randrange(4, 7)
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
        self.session_number = 0
        self.keys = pg.key.get_pressed()
        self.allsprites = pg.sprite.Group()
        self.card_sprite = pg.sprite.Group()
        self.money_sprite = pg.sprite.Group()
        self.saw_sprite = pg.sprite.Group()
        self.player = Player(self.screen_rect.center, 5, self.allsprites)
        self.score_text = None
        for _ in range(8):
            Money(self.screen_rect, self.allsprites, self.money_sprite)
        for _ in range(1):
            Bonus_Card(self.screen_rect, self.allsprites, self.card_sprite)
        for _ in range(3):
            Saw(self.screen_rect, self.allsprites, self.saw_sprite)
        joystick_count = pg.joystick.get_count()
        print ("There is ", joystick_count, " joystick's.")
        if joystick_count == 0:
            print ("No joystick's where found.")
        else:
            my_joystick = pg.joystick.Joystick(0)
            my_joystick.init()

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
            elif event.type in (pg.JOYBUTTONDOWN, pg.JOYBUTTONUP):
                h_axis_pos = my_joystick.get_axis(0)
                v_axis_pos = my_joystick.get_axis(1)
                print (h_axis_pos, v_axis_pos)
                self.rect.x = int(x + h_axis_pos * 5)
                self.rect.y = int(y + v_axis_pos * 5)
            if self.keys[pg.K_SPACE]:
                print('User let go of the space bar key')
                if not self.done:
                    self.session_number += 1
                    self.done = False
                    print("Not done!")
            elif self.keys[pg.K_l]:
                print('Lose Game!')
                self.done = False
    def render(self):
        """
        Perform all necessary drawing and update the screen.
        """
        self.screen.fill(pg.Color(51, 153, 255))
        if not self.done and self.session_number >= 1:
            if self.session_number >= 1:
                self.allsprites.draw(self.screen)
                self.screen.blit(self.score_text, (5, 5))
        else:
            self.title_screen()
        if self.player.score <= -10 and self.session_number == 0:
            self.game_over_screen()
            print(self.session_number)
        pg.display.update()

    def update(self):
        saw_hits = pg.sprite.spritecollide(self.player, self.saw_sprite, False)
        money_hits = pg.sprite.spritecollide(self.player, self.money_sprite, False)
        card_hits = pg.sprite.spritecollide(self.player, self.card_sprite, False)
        for hit in saw_hits:
            hit.reset(self.screen_rect)
            self.player.score -= 5
        for hit in money_hits:
            hit.reset(self.screen_rect)
            self.player.score += 1
        for hit in card_hits:
            hit.reset(self.screen_rect)
            self.player.score += 3
        self.update_score()
        self.allsprites.update(self.screen_rect, self.keys)

    def game_over_screen(self):
        game_over = pg.font.SysFont('serif', 25)
        click_enter = pg.font.SysFont('serif', 15)
        main_text = game_over.render('Game Over', True, pg.Color("black"))
        sub_text = \
            click_enter.render('(Click the space bar to play again)',
                               True, BLACK)
        center_x = SCREEN_SIZE[0] // 2 - main_text.get_width() // 2
        center_y = SCREEN_SIZE[1] // 2 - main_text.get_height() // 2
        screen.blit(main_text, [center_x, center_y])
        center_x = SCREEN_SIZE[0] // 2 - sub_text.get_width() // 2
        center_y = SCREEN_SIZE[1] // 2 - (sub_text.get_height() // 2
                                          - 20)
        self.screen.blit(sub_text, [center_x, center_y])

    def title_screen(self):

        # First drawn screen the user is prompted by

        new_begin = pg.font.SysFont('serif', 35)
        new_begin_sub = pg.font.SysFont('serif', 15)
        begin_text = new_begin.render('Press the space bar to play',
                                      True, pg.Color("black"))
        begin_text_sub = new_begin_sub.render('(Use arrow keys or controller to interact)',
                                              True, pg.Color("black"))
        center_x = SCREEN_SIZE[0] // 2 - begin_text.get_width() // 2
        center_y = SCREEN_SIZE[1] // 2 - begin_text.get_height() // 2
        center_x_sub = SCREEN_SIZE[0] // 2 - begin_text_sub.get_width() // 2
        center_y_sub = SCREEN_SIZE[1] // 2 - begin_text_sub.get_height() // 2 + 35
        self.screen.blit(begin_text, [center_x, center_y])
        self.screen.blit(begin_text_sub, [center_x_sub, center_y_sub])

    def update_score(self):
        score_raw = "Score: {}".format(self.player.score)
        if self.player.score  <= 0:
            self.score_text = FONT.render(score_raw, True, pg.Color("red"))
        elif self.player.score >= 1 and self.player.score <= 9:
            self.score_text = FONT.render(score_raw, True, pg.Color(255,165,0))
        elif self.player.score >= 10:
            self.score_text = FONT.render(score_raw, True, pg.Color("green"))
        else:
            self.score_text = FONT.render(score_raw, True, pg.Color("black"))

    def main_loop(self):
        """
        One game loop. Simple and clean.
        """
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(self.fps)

def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    global IMAGES, FONT
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.joystick.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE, pg.NOFRAME)
    IMAGES = load_images()
    FONT = pg.font.SysFont('Calibri', 25, True, False)
    JOYSTICKS = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
    Application().main_loop()
    pg.quit()
    pg.joystick.quit()
    sys.exit()


if __name__ == "__main__":
    main()
