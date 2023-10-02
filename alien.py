import pygame
from pygame.sprite import Sprite
import time
from random import randint

class Alien(Sprite):
    def __init__(self, ai_setting, screen):
        super(Alien, self).__init__()
        self.ai_setting = ai_setting
        self.screen = screen
        # 获取外星人的信息
        self.image = pygame.image.load('./images/alien.bmp')
        self.image_d = pygame.image.load('./images/boom.bmp')
        self.rect = self.image.get_rect()
        # self.screen_rect = screen.get_rect()
        # 每个外星人的最初都在屏幕左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """"向右移动外星人"""

        self.x += (self.ai_setting.alien_speed_factor * self.ai_setting.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """如果在边沿就返回true"""
        screen_rect = self.screen.get_rect()
        if self.rect.right > screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


