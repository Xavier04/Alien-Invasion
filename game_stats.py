class GameStats:
    """trace game states"""

    def __init__(self, ai_settings):
        """initialize stats"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        """initialize stats that might change during the game"""
        self.ship_left = self.ai_settings.ship_limit
