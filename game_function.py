import sys
from time import sleep

import json
import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, stats, ship, bullets):
    """response press"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        write_high_score(stats)
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """if not reaching limitation, fire a bullet"""
    # create a bullet, add to group bullets
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """response release"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """response the keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            write_high_score(stats)
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship,
                                 bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """start game when player hit 'play' button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset game
        ai_settings.initialize_dynamic_settings()

        # hide cursor
        pygame.mouse.set_visible(False)

        # reset game stats
        stats.reset_stats()
        stats.game_active = True

        # reset score board image
        sb.prep_score()
        sb.prep_level()
        sb.prep_high_score()
        sb.prep_ships()

        # clear aliens and bullets lists
        aliens.empty()
        bullets.empty()

        # create a new fleet and put ship at the center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """update the screen and change to new screen"""
    # redraw the screen in each circulation
    screen.fill(ai_settings.bg_color)

    # redraw all bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # show score
    sb.show_score()

    # if the game is not active, draw play button
    if not stats.game_active:
        play_button.draw_button()

    # show the latest screen
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """update bullets position and delete disappeared bullets"""
    # update bullets position
    bullets.update()

    # delete disappeared bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets):
    """response bullet and alien collisions"""
    # check if bullet hits alien, if so delete bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # delete current bullets, speed up game and regenerate a fleet
        bullets.empty()
        ai_settings.increase_speed()

        # increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def create_fleet(ai_settings, screen, ship, aliens):
    """create alien fleet"""
    # create an alien, calculate allowed aliens in a row
    # alien space is the alien width
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # create aliens in first row
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def get_number_alien_x(ai_settings, alien_width):
    # calculate allowed aliens in a row
    available_space_x = ai_settings.screen_width - 4 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """create an alien in current row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """calculate the allowed rows"""
    available_space_y = (ai_settings.screen_height
                         - 3 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    """when alien reaches edges, change direction"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """move fleet down and change their direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """response collision"""
    if stats.ship_left > 0:
        # ship_left - 1
        stats.ship_left -= 1

        # update score board
        sb.prep_ships()

        # clear the aliens and bullets
        aliens.empty()
        bullets.empty()

        # create a new fleet and put ship at the bottom center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """check if any alien reaches bottom"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # act as ship_hit
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """check if aliens reach the edges, then update positions of all aliens"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # check collision between aliens and ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # check if any aliens reach bottom
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """check if high score appear"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def write_high_score(stats):
    """write high score to file"""
    filename = 'high_score.json'

    with open(filename, 'w') as f_obj:
        json.dump(stats.high_score, f_obj)


def load_high_score(stats):
    """load high score from file"""
    filename = 'high_score.json'
    try:
        with open(filename, 'r') as f_obj:
            stats.high_score = json.load(f_obj)
    except:
        pass

