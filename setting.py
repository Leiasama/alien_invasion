class Setting:
    """"存储ALien_Invasion"""

    def __init__(self):
        # 注意双下划线
        """初始化游戏设置"""
        # 屏幕设置
        self.fleet_direction = None
        self.bullet_speed_factor = None
        self.alien_speed_factor = None
        self.ship_speed_factor = None
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (232, 206, 104)

        self.bullet_width = 6
        self.bullet_height = 10
        self.bullets_allowed = 3

        self.fleet_drop_speed = 1.5

        self.ship_limit = 3
        self.speedup_scale = 1.08
        self.initialize_dynamic_setting()
        self.alien_points = 50

    def initialize_dynamic_setting(self):
        # 初始速度
        self.ship_speed_factor = 0.55
        # 子弹设置
        self.bullet_speed_factor = 0.25
        # 外星人
        self.alien_speed_factor = 0.2
        # fleet方向 1右移，-1左移
        self.fleet_direction = 1

    def increase_speed(self):
        # 初始速度
        self.ship_speed_factor *= self.speedup_scale
        # 子弹设置
        self.bullet_speed_factor *= self.speedup_scale
        # 外星人
        self.alien_speed_factor *= self.speedup_scale
        # fleet方向 1右移，-1左移
        self.bullets_allowed += 1
        self.alien_points = int(self.alien_points*self.speedup_scale*1.2)
