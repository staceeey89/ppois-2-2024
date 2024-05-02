import random

import pygame
import sys

from engine.pause import Pause
from engine.scene import Scene
from game import (PLAYER_WIDTH, PLAYER_HEIGHT, weapons, SCREEN_WIDTH, BULLET_WIDTH, ENEMY_WIDTH, ENEMY_HEIGHT,
                  player_img, BRICK_WIDTH, SCREEN_HEIGHT, enemies, waves, WHITE, animations, BULLET_EXPLOSION_WIDTH,
                  BULLET_EXPLOSION_HEIGHT, font, BLACK, dp, ENEMY_SHOT,
                  FLAGSHIP, scores_manager, sounds)
from game.animator import Animator, Animation
from game.objects import Player, EnemyBox, WallBox, Bullet, Enemy, Brick, Lives, Flagship, DroppedWeapon
from engine.collision import Collision


class Gameplay(Scene):
    def __init__(self, *args):
        super().__init__()
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 20,
                             weapons['player_basic'])
        self.bullets = []
        self.walls = [
            WallBox(135, 600),
            WallBox(135 + BRICK_WIDTH * 4 + 115, 600),
            WallBox(135 + (BRICK_WIDTH * 4 + 115) * 2, 600),
            WallBox(135 + (BRICK_WIDTH * 4 + 115) * 3, 600)
        ]
        self.bricks = [brick for wall in self.walls for brick in wall.bricks]
        self.enemy_block = EnemyBox(
            waves[random.randint(0, len(waves) - 1)]
        )
        self.flagship = None
        self.animator = Animator()
        self.dropped_weapons = []
        self.score = 0
        self.scene = None
        self.lives = Lives(390, 22, player_img)
        self.pause = Pause()
        self.cooldown = Pause()
        pygame.time.set_timer(FLAGSHIP, 100)

    @Collision.collision(lambda self: self.bullets, lambda self: self.enemy_block.enemies)
    def enemy_col(self, bullet: Bullet, enemy: Enemy):
        if type(bullet.parent) is Player:
            print("ENEMY HIT")
            self.bullets.remove(bullet)
            self.enemy_block.kill_enemy(enemy)
            self.animator.play(Animation(x=enemy.x,
                                         y=enemy.y,
                                         width=ENEMY_WIDTH,
                                         height=ENEMY_HEIGHT,
                                         data=animations['enemy_explosion']))
            sound = pygame.mixer.Sound(sounds['hit'])
            sound.play()
            self.score += enemy.score
            if len(self.enemy_block.enemies) == 0:
                self.enemy_block = EnemyBox(
                    waves[random.randint(0, len(waves) - 1)]
                )
                sound = pygame.mixer.Sound(sounds['new_wave'])
                sound.play()

    @Collision.collision(lambda self: self.bullets, lambda self: [self.flagship])
    def flagship_col(self, bullet: Bullet, enemy: Flagship):
        if type(bullet.parent) is Player:
            self.bullets.remove(bullet)
            self.flagship = None
            sound = pygame.mixer.Sound(sounds['flagshiphit'])
            sound.play()
            self.animator.play(Animation(x=enemy.x,
                                         y=enemy.y,
                                         width=ENEMY_WIDTH,
                                         height=ENEMY_HEIGHT,
                                         data=animations['enemy_explosion']))
            if enemy.drop:
                choice = random.choice(('dropped_basic', 'dropped_advanced', 'dropped_boss'))
                weapon = weapons[choice]
                self.dropped_weapons.append(DroppedWeapon(x=enemy.x,
                                                          y=enemy.y,
                                                          data=weapon,
                                                          type_par=choice.replace('dropped_', 'player_')))
            self.score += enemy.score

    @Collision.collision(lambda self: self.dropped_weapons, lambda self: [self.player])
    def dropped_weapon_col(self, weapon: DroppedWeapon, player: Player):
        self.player.weapon = weapons[weapon.type]
        self.dropped_weapons.remove(weapon)
        sound = pygame.mixer.Sound(sounds['collect'])
        sound.play()

    @Collision.collision(lambda self: self.bullets, lambda self: self.bricks)
    def wall_col(self, bullet: Bullet, brick: Brick):
        self.bullets.remove(bullet)
        if brick.ruin():
            for wall in self.walls:
                if brick in wall.bricks:
                    wall.bricks.remove(brick)
                    self.bricks.remove(brick)
                    break
        print("hit")

    @Collision.collision(lambda self: self.bullets, lambda self: [self.player])
    def player_col(self, bullet: Bullet, player: Player):
        if type(bullet.parent) is Enemy:
            self.bullets.remove(bullet)
            self.lives.minus()
            self.animator.play(Animation(x=player.x,
                                         y=player.y,
                                         width=PLAYER_WIDTH,
                                         height=PLAYER_HEIGHT,
                                         data=animations['player_explosion']))
            self.pause.stop(180)
            sound = pygame.mixer.Sound(sounds['crash'])
            sound.play()
            self.bullets.clear()
            if self.lives.lives == 0:
                dp.checkout(GameOver, self.score)

    @Collision.collision(lambda self: self.bullets, lambda self: self.bullets)
    def bullet_col(self, bullet1: Bullet, bullet2: Bullet):
        if not isinstance(bullet1.parent, type(bullet2.parent)):
            self.bullets.remove(bullet1)
            self.bullets.remove(bullet2)
            self.animator.play(Animation(x=bullet1.x - BULLET_EXPLOSION_WIDTH / 2 + BULLET_WIDTH / 2,
                                         y=bullet1.y,
                                         width=BULLET_EXPLOSION_WIDTH,
                                         height=BULLET_EXPLOSION_HEIGHT,
                                         data=animations['bullet_explosion']))

    def handle_collisions(self):
        self.enemy_col()
        self.bullet_col()
        self.player_col()
        self.wall_col()
        self.dropped_weapon_col()
        if self.flagship:
            self.flagship_col()

    def render(self, src):
        src.fill(WHITE)
        if not self.pause():
            self.player.draw()
        self.enemy_block.draw()
        for wall in self.walls:
            wall.draw()
        for bullet in self.bullets:
            bullet.draw()
        for dropped_weapon in self.dropped_weapons:
            dropped_weapon.draw()
        self.animator()
        self.score_text(src)
        self.lives()
        if self.flagship:
            self.flagship.draw()

        pygame.display.update()

    def score_text(self, src):
        score_text = font.render("SCORE " + str(self.score), True, BLACK)
        src.blit(score_text, (10, 20))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # if event.key == pygame.K_END:
                #     dp.checkout(GameOver, self.score)
                # if event.key == pygame.K_UP:
                #     pygame.time.set_timer(ENEMY_SHOT, 100)
                elif event.key == pygame.K_SPACE:
                    if not self.pause() and not self.cooldown():
                        self.bullets.extend(self.player.shoot())
                        self.cooldown.stop(20)
                elif event.key == pygame.K_m:
                    dp.checkout(MainMenu)
            if event.type == ENEMY_SHOT:
                if not self.pause():
                    self.bullets.extend(self.enemy_block.shoot())
            if event.type == FLAGSHIP:
                direction = random.choice((-1, 1))
                if direction < 0:
                    x = SCREEN_WIDTH + 100
                else:
                    x = -100
                if self.flagship is None:
                    choice = random.choice(('flagship', 'toother'))
                    self.flagship = Flagship(x,
                                             100,
                                             enemies[choice], 5 * direction,
                                             False if choice == 'toother' else True)
        if not self.pause():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()

            for bullet in self.bullets:
                bullet.move()
                if bullet.y < 0:
                    self.bullets.remove(bullet)
                if bullet.y > SCREEN_HEIGHT:
                    self.bullets.remove(bullet)

            for dropped_weapon in self.dropped_weapons:
                dropped_weapon.move()
                if dropped_weapon.y > SCREEN_HEIGHT:
                    self.dropped_weapons.remove(dropped_weapon)

            if self.flagship:
                self.flagship.move()
                if self.flagship.x < - 300 or self.flagship.x > SCREEN_WIDTH + 300:
                    self.flagship = None

            self.enemy_block.move()
            self.handle_collisions()

        self.pause.frame()
        self.cooldown.frame()


class MainMenu(Scene):
    def __init__(self, *args):
        super().__init__()
        self.play_text = font.render("Press SPACE to Play", True, BLACK)

        self.help_text = font.render("Press 'H' for Help", True, BLACK)
        self.leaderboard_text = font.render("Press 'T' for Leaderboard", True, BLACK)
        self.exit_text = font.render("Press 'ESC' to Exit", True, BLACK)

        self.bottom_text = font.render("SPACE INVADERS GAME!", True, BLACK)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    dp.checkout(Gameplay)
                if event.key == pygame.K_h:
                    dp.checkout(HelpPage)
                if event.key == pygame.K_t:
                    dp.checkout(Leaderboard)

    def render(self, scr):
        scr.fill(WHITE)
        play_text_rect = self.play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        scr.blit(self.play_text, play_text_rect)

        help_text_rect = self.help_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        scr.blit(self.help_text, help_text_rect)

        leaderboard_text_rect = self.leaderboard_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        scr.blit(self.leaderboard_text, leaderboard_text_rect)

        exit_text_rect = self.exit_text.get_rect(center=(SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3))
        scr.blit(self.exit_text, exit_text_rect)

        bottom_text_rect = self.bottom_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        scr.blit(self.bottom_text, bottom_text_rect)

        pygame.display.update()


class GameOver(Scene):
    def __init__(self, score, *args):
        super().__init__()
        self.score = score[0]
        self.max_score = scores_manager.get_max_score()
        sound = pygame.mixer.Sound(sounds['gameover'])
        sound.play()
        self.game_over = font.render("GAME OVER", True, BLACK)
        self.play_text = font.render("Press SPACE to play again", True, BLACK)
        self.bottom_text = font.render("Your game description or credits here", True, BLACK)

    def update(self):
        if self.score > self.max_score:
            dp.checkout(GameOverRecord, self.score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    dp.checkout(Gameplay)
                if event.key == pygame.K_m:
                    dp.checkout(MainMenu)

    def render(self, scr):
        scr.fill(WHITE)
        game_over_rect = self.game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        play_text_rect = self.play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        scr.blit(self.game_over, game_over_rect)
        scr.blit(self.play_text, play_text_rect)
        pygame.display.update()


class GameOverRecord(Scene):
    def __init__(self, score, *args):
        super().__init__()
        self.game_over = font.render("NEW RECORD!", True, BLACK)
        self.play_text = font.render("Press SPACE to play again", True, BLACK)

        self.name_text = font.render("Enter your name:", True, BLACK)
        self.input_text = ''
        self.input_font = pygame.font.Font(None, 32)
        self.input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 32)
        self.input_active = True
        self.score = score[0]
        sound = pygame.mixer.Sound(sounds['gameover_record'])
        sound.play()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    dp.checkout(Gameplay)
                if event.key == pygame.K_m:
                    dp.checkout(MainMenu)
                if event.key == pygame.K_RETURN:
                    name = self.input_text.strip()
                    if name:
                        scores_manager.add_score(name,
                                                 self.score)
                        dp.checkout(MainMenu)

                if self.input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

    def render(self, scr):
        scr.fill(WHITE)
        game_over_rect = self.game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        play_text_rect = self.play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        scr.blit(self.game_over, game_over_rect)
        scr.blit(self.play_text, play_text_rect)

        name_text_rect = self.name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        scr.blit(self.name_text, name_text_rect)
        pygame.draw.rect(scr, BLACK, self.input_rect, 2)
        input_surface = self.input_font.render(self.input_text, True, BLACK)
        scr.blit(input_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        pygame.display.update()


class Leaderboard(Scene):
    def __init__(self, *args):
        super().__init__()
        self.leaderboard_text = font.render("Leaderboard", True, BLACK)
        self.menu_text = font.render("Press 'M' to go back to Main Menu", True, BLACK)
        self.records = scores_manager.load_scores()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_m:
                    dp.checkout(MainMenu)

    def render(self, scr):
        scr.fill(WHITE)
        leaderboard_rect = self.leaderboard_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        scr.blit(self.leaderboard_text, leaderboard_rect)

        y_offset = 120
        sorted_records = sorted(self.records.items(), key=lambda x: x[1], reverse=True)
        for i, (name, score) in enumerate(sorted_records[:10], start=1):
            record_text = font.render(f"{i}. {name}: {score}", True, BLACK)
            record_rect = record_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            scr.blit(record_text, record_rect)
            y_offset += 50

        menu_rect = self.menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        scr.blit(self.menu_text, menu_rect)

        pygame.display.update()


class HelpPage(Scene):
    def __init__(self, *args):
        super().__init__()
        self.title_text = font.render("Space Invaders - Help", True, BLACK)
        self.rules_text = [
            font.render("Welcome to Space Invaders!", True, BLACK),
            font.render("Objective:", True, BLACK),
            font.render("Defend the Earth from invading", True, BLACK),
            font.render("alien spaceships by", True, BLACK),
            font.render("shooting them down.", True, BLACK),
            font.render("Controls:", True, BLACK),
            font.render("Use the 'ARROW' keys to move", True, BLACK),
            font.render("left and right.", True, BLACK),
            font.render("Press the 'SPACE' to fire", True, BLACK),
            font.render("missiles at the aliens.", True, BLACK),
            font.render("Avoid being hit by the", True, BLACK),
            font.render("aliens' projectiles.", True, BLACK),
            font.render("Game Over:", True, BLACK),
            font.render("The game ends when", True, BLACK),
            font.render("all of your lives", True, BLACK),
            font.render("are lost.", True, BLACK),
            font.render("Press 'M' to return to main menu.", True, BLACK),
            font.render("Press 'ESC' to exit at any time.", True, BLACK),
        ]

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_m:
                    dp.checkout(MainMenu)

    def render(self, scr):
        scr.fill(WHITE)
        title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        scr.blit(self.title_text, title_rect)

        y_offset = 120
        for text_surface in self.rules_text:
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            scr.blit(text_surface, text_rect)
            y_offset += 35

        pygame.display.update()
