import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_setting, screen, stats):
        super(Ship, self).__init__()
        """设置飞船并初始化其位置"""
        self.screen = screen
        self.ai_setting = ai_setting

        # 加载飞船图像并获得取外接矩形
        self.image = pygame.image.load("images/ship.bmp")
        self.image_dead = pygame.image.load('./images/death.bmp')
        self.rect = self.image.get_rect()
        # 飞船的方形
        self.screen_rect = screen.get_rect()
        self.stats = stats
        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.centerx = float(self.rect.centerx)
        # x 坐标
        self.centery = float(self.rect.bottom - self.rect.height * 0.5)
        # y 坐标,需要手动调整
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_ahead = False
        self.moving_behind = False

    def update(self):
        """根据移动标志更改飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_setting.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_setting.ship_speed_factor
        if self.moving_ahead and self.rect.top > self.screen_rect.top:
            self.centery -= self.ai_setting.ship_speed_factor
        if self.moving_behind and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_setting.ship_speed_factor

        # 每次更新
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blit_me(self):
        """"指定位置重绘飞船"""
        self.stats.ship_left == self.ai_setting.ship_limit if self.screen.blit(self.image,
                                                                               self.rect) else self.screen.blit(
            self.image_dead, self.rect)

    def center_ship(self):
        """飞船居中"""
        self.centerx = self.screen_rect.centerx
        self.centery = float(self.screen_rect.bottom - self.rect.height * 0.5)
