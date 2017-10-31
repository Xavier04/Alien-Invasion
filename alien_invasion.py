import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_function as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # initialize game and create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # create 'play' button
    play_button = Button(ai_settings, screen, 'play')

    # create object to store game stats
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # create a ship
    ship = Ship(ai_settings, screen)
    # create a group to store bullet
    bullets = Group()
    # create an alien group
    aliens = Group()

    # create aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # begin the main circulation of the game
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens,
                        bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)


if __name__ == '__main__':
    run_game()
