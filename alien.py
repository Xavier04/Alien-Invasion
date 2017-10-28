import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """class for single alien"""

    def __init__(self, ai_settings, screen):
        """initialize alien and set the original position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load alien image and set rect property
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # the original position of each alien is on the top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the exact position of alien
        self.x = float(self.rect.x)

    def blitme(self):
        """draw alien at specified position"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """alien move right"""
        self.x += (self.ai_settings.alien_speed_factor
                   * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """if aliens reach edges, return True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
