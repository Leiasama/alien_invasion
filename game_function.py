import sys
from random import randint
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet


def check_keydown_event(event, ai_setting, screen, ship, bullets):
    # RIGHT
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    # LEFT
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # UP
    elif event.key == pygame.K_UP:
        ship.moving_ahead = True
    # DOWN
    elif event.key == pygame.K_DOWN:
        ship.moving_behind = True
        # 创建子弹并将其输入到bullets编组里
    # SPACE
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_setting, screen, ship, bullets)
    # ESC
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_event(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_ahead = False
    elif event.key == pygame.K_DOWN:
        ship.moving_behind = False
    # 响应松开


def check_event(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets):
    """响应按键和鼠标"""
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:

            check_keydown_event(event, ai_setting, screen, ship, bullets)

        elif event.type == pygame.KEYUP:

            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_setting, screen, stats, sb, ship, bullets, aliens, play_button):
    """循环重绘"""
    screen.fill(ai_setting.bg_color)
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blit_me()
    for alien in aliens.sprites():
        alien.blitme()
    # 如果不处于活动状态 就画play
    if not stats.game_active and stats.ship_left > 0:
        play_button.draw_button()
    if stats.ship_left < 0:
        play_button.draw_fail()
    # 屏幕可见
    pygame.display.flip()


def update_bullets(ai_setting, screen, stats, sb, ship, aliens, bullets):
    """"更新子弹的位置并删除子弹"""
    bullets.update()

    # 删除离开屏幕的子弹以免造成浪费
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_setting, screen, stats, sb, ship, aliens, bullets)


def fire_bullets(ai_setting, screen, ship, bullets):
    """"如果没有到到达限制就发射子弹"""
    if len(bullets) <= ai_setting.bullets_allowed:
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_setting, screen, ship, aliens):
    """"创建外星人群"""
    # 先建一个外星人再算能容纳多少外星人
    alien = Alien(ai_setting, screen)
    number_alien_x = get_number_alien_x(ai_setting, alien.rect.width)
    number_rows = get_number_row(ai_setting, ship.rect.height, alien.rect.height)
    # 创建外星人
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_setting, screen, aliens, alien_number, row_number)


def get_number_alien_x(ai_setting, alien_width):
    """"计算每行走多少外星人"""
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def create_alien(ai_setting, screen, aliens, alien_number, row_number):
    """"创建外星人并放在当前行"""
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_row(ai_setting, ship_height, alien_height):
    """"计算屏幕可以放多少行"""
    available_space_y = (ai_setting.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_setting, aliens):
    """"外星人碰壁时候的措施"""
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break


def change_fleet_direction(ai_setting, aliens):
    """整个外星人向下移，并改变其方向"""
    for alien in aliens.sprites():
        random_number = randint(1, 9)
        alien.rect.y += ai_setting.fleet_drop_speed * random_number
    ai_setting.fleet_direction *= -1


def update_aliens(ai_setting, stats, screen, sb, ship, aliens, bullets):
    """检查外星人是否在屏幕边沿，并更新外星人的位置"""
    check_fleet_edges(ai_setting, aliens)
    aliens.update()
    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, stats, screen, sb, ship, aliens, bullets)
    # 检查触底
    check_aliens_bottom(ai_setting, stats, screen, sb, ship, aliens, bullets)
    # 检查碰撞


def check_bullet_alien_collisions(ai_setting, screen, stats, sb, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 删除外星人和子弹
    # 子弹与外星人碰撞
    collisions_ba = pygame.sprite.groupcollide(aliens, bullets, True, True)
    if collisions_ba:
        for aliens in collisions_ba.values():
            stats.score += ai_setting.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # 删除现有子弹创建外星人
        bullets.empty()
        stats.level += 1
        sb.prep_level()
        ai_setting.increase_speed()
        create_fleet(ai_setting, screen, ship, aliens)


def ship_hit(ai_setting, stats, screen, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    stats.ship_left -= 1
    if stats.ship_left >= 0:
        sb.prep_ship()
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人

        create_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_setting, stats, screen, sb, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, stats, screen, sb, ship, aliens, bullets)
            break


def check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """单击按钮开始游戏或退出"""
    button_cliked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_cliked and not stats.game_active:
        ai_setting.initialize_dynamic_setting()
        if stats.ship_left > 0:
            pygame.mouse.set_visible(False)
            stats.reset_stats()
            stats.game_active = True
            # 重置记分牌
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ship()
            # 清空外星人列表和子弹列表
            aliens.empty()
            bullets.empty()
            # 创建新的外星人，让飞船居中
            create_fleet(ai_setting, screen, ship, aliens)
            ship.center_ship()
        else:
            sys.exit()


def check_high_score(stats, sb):
    """检查最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
