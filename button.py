import pygame.font


class Button():
    def __init__(self, ai_setting, screen, msg):
        """初始化信息按钮"""

        self.font = pygame.font.SysFont(None, 48)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load('./images/start.bmp')
        self.image_fail = pygame.image.load('./images/failed.bmp')
        self.image_rect = self.image.get_rect()
        self.width, self.height = 200, 50
        self.text_color = (255, 255, 255)
        self.rect = pygame.Rect(0, 0, self.image_rect.width, self.image_rect.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将文字渲染成图像并在按钮上"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        self.image_rect.centerx = self.msg_image_rect.centerx
        self.image_rect.centery = self.msg_image_rect.centery

    def draw_button(self):
        """"画按钮"""
        self.screen.blit(self.image, self.image_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_fail(self):
        """"画按钮"""
        self.screen.blit(self.image_fail, self.image_rect)
        self.screen.blit(self.font.render("LOSE", True, self.text_color), self.msg_image_rect)
