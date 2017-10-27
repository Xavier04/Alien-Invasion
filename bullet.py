import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """manage the bullet fired by ship"""

    def __init__(self, ai_settings, screen, ship):
        """create a bullet object at the position of ship"""
        super().__init__()
        self.screen = screen

        # create a bullet rectangle at (0, 0), then set the right location
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store bullet position in float
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """move up"""
        # update the bullet y coordinate
        self.y -= self.speed_factor
        # update the bullet rect
        self.rect.y = self.y

    def draw_bullet(self):
        """draw bullet on screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
