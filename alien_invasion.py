import PIL.Image
import pygame

from scoreboard import Scoreboard
from setting import Setting
from ship import Ship
from pygame.sprite import Group
import game_function as gf
from game_stats import Game_states
from button import Button

img = PIL.Image.open('images/1715803_planet_space_uranus_icon.ico')
img = img.tobytes(), img.size, img.mode


# 逼pygame持续响应

# 绷不住 ico必须用pil改格式才给换


def run_game():
    # 初始化游戏并建立屏幕对象
    pygame.init()
    ai_setting = Setting()
    screen = pygame.display.set_mode(
        (ai_setting.screen_width, ai_setting.screen_height))
    # 设置名和图标
    pygame.display.set_caption("Emotional Damage")
    play_button = Button(ai_setting, screen, "Play")
    # 创建状态
    stats = Game_states(ai_setting)
    pygame.display.set_icon(pygame.image.frombytes(*img))
    sb = Scoreboard(ai_setting, screen, stats)
    # 创建飞船
    ship = Ship(ai_setting, screen,stats)
    # 创建子弹
    bullets = Group()
    # 创建外星人
    aliens = Group()

    gf.create_fleet(ai_setting, screen, ship, aliens)

    # 绷不住逼分辨率这么小
    # 游戏循环
    while True:
        # pygame.key.set_repeat(10)
        # 传参不导包
        gf.check_event(ai_setting, screen, stats, sb,play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_setting, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_setting, stats, screen, sb,ship, aliens, bullets)
        # print(len(bullets))
        gf.update_screen(ai_setting, screen, stats, sb, ship, bullets, aliens, play_button)


run_game()
