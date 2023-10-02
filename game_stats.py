class Game_states:
    """跟踪游戏状态"""

    def __init__(self, ai_setting):
        """初始化统计信息"""
        self.score = None
        self.ship_left = None
        self.ai_setting = ai_setting
        self.reset_stats()
        self.game_active = False
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """初始化游戏信息"""
        self.ship_left = self.ai_setting.ship_limit
        self.score = 0
