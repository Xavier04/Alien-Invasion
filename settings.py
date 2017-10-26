class Settings:
    """store all settings in Alien Invasion"""

    def __init__(self):
        """initialize game settings"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_speed_factor = 1.5
