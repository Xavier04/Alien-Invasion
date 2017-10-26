import pygame


class Ship:

    def __init__(self, ai_settings, screen):
        """initialize ship and set the beginning position"""
        self.screen = screen
        self.ai_settings = ai_settings

        # load ship image and get the circumscribed rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # put every new ship at the center of screen bottom
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store float in the ship property 'center'
        self.center = float(self.rect.centerx)

        # moving flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """adjust ship position according to moving flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # update rect according to self.center
        self.rect.centerx = self.center

    def blitme(self):
        """draw ship in the specified position"""
        self.screen.blit(self.image, self.rect)
