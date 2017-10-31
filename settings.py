class Settings:
    """store all settings in Alien Invasion"""

    def __init__(self):
        """initialize game static settings"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 3

        # how fast that game accelerates
        self.speedup_scale = 1.1
        # alien point increase speed
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings changing with game proceed"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        # alien settings
        self.fleet_drop_speed = 10
        self.alien_speed_factor = 1

        # fleet_direction = 1, move right; = -1 move right
        self.fleet_direction = 1

        # score
        self.alien_points = 50

    def increase_speed(self):
        """increase speed settings and alien point"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

