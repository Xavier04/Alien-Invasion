class GameStats:
    """trace game states"""

    def __init__(self, ai_settings):
        """initialize stats"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # game is not active at the beginning
        self.game_active = False

    def reset_stats(self):
        """initialize stats that might change during the game"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
