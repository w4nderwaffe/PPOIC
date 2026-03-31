from pathlib import Path
import random
import pygame

from src.states.base_state import BaseState
from src.core.settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BULLET_COOLDOWN,
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    PLAYER_START_LIVES,
    BUNKER_COUNT,
    BUNKER_BLOCK_SIZE,
    BUNKER_START_Y,
    ENEMY_SHOOT_INTERVAL_MIN,
    ENEMY_SHOOT_INTERVAL_MAX,
    EXPLOSION_DURATION,
    PLAYER_EXPLOSION_DURATION,
    SAUCER_SPAWN_MIN,
    SAUCER_SPAWN_MAX,
    DOUBLE_FIRE_DURATION,
    DOUBLE_FIRE_COOLDOWN
)
from src.entities.player import Player
from src.entities.bullet import Bullet
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet
from src.entities.bunker import Bunker
from src.entities.explosion import Explosion
from src.entities.saucer import Saucer
from src.data.config_loader import ConfigLoader
from src.ui.text_renderer import TextRenderer
from src.ui.neon_draw import draw_glow_line, draw_glow_rect


class PlayState(BaseState):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)

        self.game.sound_manager.stop_music()

        self.ui_font = TextRenderer.load_font(26)
        self.small_font = TextRenderer.load_font(18)
        self.wave_font = TextRenderer.load_font(42)

        self.background = self.load_background()

        self.player = Player()
        self.bullets = []
        self.enemy_bullets = []
        self.explosions = []

        self.move_left = False
        self.move_right = False
        self.shooting = False

        self.base_shoot_cooldown = BULLET_COOLDOWN
        self.time_since_last_shot = self.base_shoot_cooldown

        self.score = 0
        self.lives = PLAYER_START_LIVES
        self.wave = 1

        self.saucers_destroyed = 0
        self.double_fire_timer = 0.0

        self.waves_config = ConfigLoader.load_json("config/waves.json")
        enemies_data = ConfigLoader.load_json("config/enemies.json")
        self.enemy_configs = {item["id"]: item for item in enemies_data["types"]}

        self.current_wave_config = self.get_wave_config(self.wave)

        self.enemy_move_timer = 0.0
        self.enemy_move_interval = self.current_wave_config["enemy_move_interval"]
        self.enemy_horizontal_step = self.current_wave_config["enemy_horizontal_step"]
        self.enemy_vertical_step = self.current_wave_config["enemy_vertical_step"]
        self.enemy_direction = 1

        self.enemy_shot_timer = 0.0
        self.enemy_shoot_interval_min = self.current_wave_config.get("enemy_shoot_interval_min", ENEMY_SHOOT_INTERVAL_MIN)
        self.enemy_shoot_interval_max = self.current_wave_config.get("enemy_shoot_interval_max", ENEMY_SHOOT_INTERVAL_MAX)
        self.enemy_shot_interval = random.uniform(self.enemy_shoot_interval_min, self.enemy_shoot_interval_max)

        self.wave_score_bonus = self.current_wave_config["wave_score_bonus"]
        self.wave_banner_timer = 2.0

        self.saucer = None
        self.saucer_spawn_timer = 0.0
        self.saucer_spawn_interval = random.uniform(SAUCER_SPAWN_MIN, SAUCER_SPAWN_MAX)

        self.enemies = []
        self.bunkers = []
        self.create_wave()
        self.create_bunkers()

    def load_background(self):
        path = Path("assets/images/game_background.png")

        if not path.exists():
            return None

        try:
            image = pygame.image.load(str(path)).convert()
            image = pygame.transform.rotate(image, 90)
            return pygame.transform.smoothscale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except pygame.error:
            return None

    def get_wave_config(self, wave_number):
        if wave_number <= len(self.waves_config):
            return self.waves_config[wave_number - 1]
        return self.waves_config[-1]

    def apply_wave_config(self):
        self.current_wave_config = self.get_wave_config(self.wave)
        self.enemy_move_interval = self.current_wave_config["enemy_move_interval"]
        self.enemy_horizontal_step = self.current_wave_config["enemy_horizontal_step"]
        self.enemy_vertical_step = self.current_wave_config["enemy_vertical_step"]
        self.enemy_shoot_interval_min = self.current_wave_config.get("enemy_shoot_interval_min", ENEMY_SHOOT_INTERVAL_MIN)
        self.enemy_shoot_interval_max = self.current_wave_config.get("enemy_shoot_interval_max", ENEMY_SHOOT_INTERVAL_MAX)
        self.wave_score_bonus = self.current_wave_config["wave_score_bonus"]
        self.enemy_shot_interval = random.uniform(self.enemy_shoot_interval_min, self.enemy_shoot_interval_max)

    def create_wave(self):
        self.enemies = []

        rows = self.current_wave_config["rows"]
        columns = self.current_wave_config["columns"]
        start_x = self.current_wave_config["start_x"]
        start_y = self.current_wave_config["start_y"]
        spacing_x = self.current_wave_config["spacing_x"]
        spacing_y = self.current_wave_config["spacing_y"]

        step_x = ENEMY_WIDTH + spacing_x
        step_y = ENEMY_HEIGHT + spacing_y

        for row in range(rows):
            for col in range(columns):
                x = start_x + col * step_x
                y = start_y + row * step_y
                enemy_type = (row * columns + col + self.wave - 1) % 10
                enemy_config = self.enemy_configs[enemy_type]
                self.enemies.append(Enemy(x, y, enemy_type, enemy_config, col))

    def create_bunkers(self):
        self.bunkers = []

        bunker_width = 8 * BUNKER_BLOCK_SIZE
        total_width = BUNKER_COUNT * bunker_width
        gap_count = BUNKER_COUNT - 1
        free_space = WINDOW_WIDTH - 120 - total_width
        gap = free_space // gap_count if gap_count > 0 else 0

        start_x = 60

        for index in range(BUNKER_COUNT):
            x = start_x + index * (bunker_width + gap)
            self.bunkers.append(Bunker(x, BUNKER_START_Y))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from src.states.menu_state import MenuState
                self.state_manager.set_state(MenuState(self.game, self.state_manager))
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.move_left = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.move_right = True
            elif event.key == pygame.K_SPACE:
                self.shooting = True
                self.try_shoot()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.move_left = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.move_right = False
            elif event.key == pygame.K_SPACE:
                self.shooting = False

    def get_current_shoot_cooldown(self):
        if self.double_fire_timer > 0:
            return DOUBLE_FIRE_COOLDOWN
        return self.base_shoot_cooldown

    def try_shoot(self):
        current_cooldown = self.get_current_shoot_cooldown()

        if self.time_since_last_shot < current_cooldown:
            return

        bullet_x, bullet_y = self.player.get_bullet_spawn_position()

        if self.double_fire_timer > 0:
            self.bullets.append(Bullet(bullet_x - 12, bullet_y))
            self.bullets.append(Bullet(bullet_x + 12, bullet_y))
        else:
            self.bullets.append(Bullet(bullet_x, bullet_y))

        self.time_since_last_shot = 0.0
        self.game.sound_manager.play("shoot")

    def try_enemy_shoot(self, dt):
        self.enemy_shot_timer += dt

        if self.enemy_shot_timer < self.enemy_shot_interval:
            return

        self.enemy_shot_timer = 0.0
        self.enemy_shot_interval = random.uniform(self.enemy_shoot_interval_min, self.enemy_shoot_interval_max)

        if not self.enemies:
            return

        columns = {}

        for enemy in self.enemies:
            column = enemy.column
            if column not in columns or enemy.rect.bottom > columns[column].rect.bottom:
                columns[column] = enemy

        shooters = list(columns.values())

        if not shooters:
            return

        weights = [enemy.get_fire_weight() for enemy in shooters]
        shooter = random.choices(shooters, weights=weights, k=1)[0]
        bullet_x, bullet_y = shooter.get_bullet_spawn_position()
        self.enemy_bullets.append(EnemyBullet(bullet_x, bullet_y))

    def update_saucer(self, dt):
        self.saucer_spawn_timer += dt

        if self.saucer is None and self.saucer_spawn_timer >= self.saucer_spawn_interval:
            self.saucer = Saucer()
            self.saucer_spawn_timer = 0.0
            self.saucer_spawn_interval = random.uniform(SAUCER_SPAWN_MIN, SAUCER_SPAWN_MAX)

        if self.saucer is not None:
            self.saucer.update(dt)
            if not self.saucer.is_active:
                self.saucer = None

    def activate_double_fire_if_needed(self):
        if self.saucers_destroyed > 0 and self.saucers_destroyed % 2 == 0:
            self.double_fire_timer = DOUBLE_FIRE_DURATION

    def add_enemy_explosion(self, x, y, radius=24):
        self.explosions.append(Explosion(x, y, EXPLOSION_DURATION, radius))

    def add_player_explosion(self):
        self.explosions.append(
            Explosion(
                self.player.rect.centerx,
                self.player.rect.centery,
                PLAYER_EXPLOSION_DURATION,
                40
            )
        )

    def add_saucer_explosion(self):
        if self.saucer is None:
            return

        self.explosions.append(
            Explosion(
                self.saucer.rect.centerx,
                self.saucer.rect.centery,
                0.45,
                30
            )
        )

    def update_explosions(self, dt):
        for explosion in self.explosions:
            explosion.update(dt)
        self.explosions = [explosion for explosion in self.explosions if explosion.is_active]

    def update(self, dt):
        self.time_since_last_shot += dt

        if self.wave_banner_timer > 0:
            self.wave_banner_timer -= dt

        if self.double_fire_timer > 0:
            self.double_fire_timer -= dt
            if self.double_fire_timer < 0:
                self.double_fire_timer = 0

        if self.shooting:
            self.try_shoot()

        self.player.update(dt, self.move_left, self.move_right)

        for enemy in self.enemies:
            enemy.update(dt)

        for bullet in self.bullets:
            bullet.update(dt)

        for bullet in self.enemy_bullets:
            bullet.update(dt)

        self.bullets = [bullet for bullet in self.bullets if bullet.is_active]
        self.enemy_bullets = [bullet for bullet in self.enemy_bullets if bullet.is_active]

        self.update_enemy_formation(dt)
        self.try_enemy_shoot(dt)
        self.update_saucer(dt)
        self.handle_bullet_enemy_collisions()
        self.handle_bullet_saucer_collisions()
        self.handle_player_bullet_bunker_collisions()
        self.handle_enemy_bullet_bunker_collisions()
        self.handle_enemy_bullet_player_collisions()
        self.handle_enemy_bunker_collisions()
        self.check_wave_complete()
        self.check_game_over()
        self.update_explosions(dt)

    def update_enemy_formation(self, dt):
        self.enemy_move_timer += dt

        if self.enemy_move_timer < self.enemy_move_interval:
            return

        self.enemy_move_timer = 0.0

        if not self.enemies:
            return

        min_x = min(enemy.rect.left for enemy in self.enemies)
        max_x = max(enemy.rect.right for enemy in self.enemies)

        hit_left_edge = self.enemy_direction < 0 and min_x - self.enemy_horizontal_step <= 20
        hit_right_edge = self.enemy_direction > 0 and max_x + self.enemy_horizontal_step >= WINDOW_WIDTH - 20

        if hit_left_edge or hit_right_edge:
            for enemy in self.enemies:
                enemy.move_down(self.enemy_vertical_step)
            self.enemy_direction *= -1
        else:
            for enemy in self.enemies:
                enemy.move_horizontal(self.enemy_horizontal_step * self.enemy_direction)

    def handle_bullet_enemy_collisions(self):
        for bullet in self.bullets:
            if not bullet.is_active:
                continue

            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullet.is_active = False
                    enemy_died = enemy.take_hit()
                    if enemy_died:
                        self.score += enemy.get_score()
                        self.add_enemy_explosion(enemy.rect.centerx, enemy.rect.centery)
                        self.game.sound_manager.play("enemy_hit")
                    else:
                        self.add_enemy_explosion(enemy.rect.centerx, enemy.rect.centery, 14)
                    break

        self.bullets = [bullet for bullet in self.bullets if bullet.is_active]
        self.enemies = [enemy for enemy in self.enemies if enemy.is_alive]

    def handle_bullet_saucer_collisions(self):
        if self.saucer is None:
            return

        for bullet in self.bullets:
            if bullet.is_active and bullet.rect.colliderect(self.saucer.rect):
                bullet.is_active = False
                self.score += self.saucer.score_value
                self.saucers_destroyed += 1
                self.add_saucer_explosion()
                self.activate_double_fire_if_needed()
                self.saucer = None
                self.game.sound_manager.play("enemy_hit")
                break

        self.bullets = [bullet for bullet in self.bullets if bullet.is_active]

    def handle_player_bullet_bunker_collisions(self):
        for bullet in self.bullets:
            if not bullet.is_active:
                continue

            for bunker in self.bunkers:
                hit = False

                for block in bunker.get_alive_blocks():
                    if bullet.rect.colliderect(block.rect):
                        bullet.is_active = False
                        block.is_alive = False
                        self.explosions.append(Explosion(block.rect.centerx, block.rect.centery, 0.12, 10))
                        hit = True
                        break

                if hit:
                    break

        self.bullets = [bullet for bullet in self.bullets if bullet.is_active]

    def handle_enemy_bullet_bunker_collisions(self):
        for bullet in self.enemy_bullets:
            if not bullet.is_active:
                continue

            for bunker in self.bunkers:
                hit = False

                for block in bunker.get_alive_blocks():
                    if bullet.rect.colliderect(block.rect):
                        bullet.is_active = False
                        block.is_alive = False
                        self.explosions.append(Explosion(block.rect.centerx, block.rect.centery, 0.12, 10))
                        hit = True
                        break

                if hit:
                    break

        self.enemy_bullets = [bullet for bullet in self.enemy_bullets if bullet.is_active]

    def handle_enemy_bullet_player_collisions(self):
        for bullet in self.enemy_bullets:
            if bullet.rect.colliderect(self.player.rect):
                bullet.is_active = False
                self.lives -= 1
                self.add_player_explosion()
                self.game.sound_manager.play("player_dead")
                self.reset_after_player_hit()
                break

        self.enemy_bullets = [bullet for bullet in self.enemy_bullets if bullet.is_active]

    def handle_enemy_bunker_collisions(self):
        for enemy in self.enemies:
            for bunker in self.bunkers:
                for block in bunker.get_alive_blocks():
                    if enemy.rect.colliderect(block.rect):
                        block.is_alive = False
                        self.explosions.append(Explosion(block.rect.centerx, block.rect.centery, 0.12, 10))

    def check_wave_complete(self):
        if self.enemies:
            return

        self.score += self.wave_score_bonus

        if self.wave < len(self.waves_config):
            self.wave += 1
            self.apply_wave_config()
            self.wave_banner_timer = 2.0
            self.enemy_bullets.clear()
            self.bullets.clear()
            self.enemy_direction = 1
            self.enemy_move_timer = 0.0
            self.enemy_shot_timer = 0.0
            self.create_wave()
        else:
            from src.states.game_over_state import GameOverState
            self.state_manager.set_state(GameOverState(self.game, self.state_manager, self.score))

    def check_game_over(self):
        for enemy in self.enemies:
            if enemy.rect.bottom >= self.player.rect.top:
                self.lives -= 1
                self.add_player_explosion()
                self.game.sound_manager.play("player_dead")
                self.reset_after_player_hit()
                break

    def reset_after_player_hit(self):
        if self.lives <= 0:
            from src.states.game_over_state import GameOverState
            self.state_manager.set_state(GameOverState(self.game, self.state_manager, self.score))
            return

        self.player = Player()
        self.bullets.clear()
        self.enemy_bullets.clear()
        self.shooting = False
        self.enemy_direction = 1
        self.enemy_move_timer = 0.0
        self.enemy_shot_timer = 0.0
        self.enemy_shot_interval = random.uniform(self.enemy_shoot_interval_min, self.enemy_shoot_interval_max)
        self.create_wave()
        self.create_bunkers()

    def draw_background_overlay(self, screen):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 95), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(overlay, (0, 0))

    def draw_lives(self, screen):
        base_x = WINDOW_WIDTH - 190
        y = 24

        for index in range(self.lives):
            body_rect = pygame.Rect(base_x + index * 52, y + 12, 38, 18)
            turret_start = (base_x + index * 52 + 19, y)
            turret_end = (base_x + index * 52 + 19, y + 12)

            draw_glow_rect(screen, body_rect, (255, 150, 255), (180, 60, 255))
            draw_glow_line(screen, turret_start, turret_end, (255, 150, 255), 4, (180, 60, 255))

    def draw_bottom_line(self, screen):
        draw_glow_line(
            screen,
            (40, WINDOW_HEIGHT - 25),
            (WINDOW_WIDTH - 40, WINDOW_HEIGHT - 25),
            (255, 150, 255),
            3,
            (180, 60, 255)
        )

    def draw_wave_banner(self, screen):
        if self.wave_banner_timer <= 0:
            return

        text = TextRenderer.render_neon_text(
            self.wave_font,
            f"WAVE {self.wave}",
            (255, 255, 255),
            (180, 60, 255)
        )
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text, rect)

    def draw_double_fire_label(self, screen):
        if self.double_fire_timer <= 0:
            return

        text = TextRenderer.render_neon_text(
            self.small_font,
            f"DOUBLE FIRE {self.double_fire_timer:.1f}",
            (255, 255, 255),
            (180, 60, 255)
        )
        screen.blit(text, (WINDOW_WIDTH // 2 - 110, 70))

    def draw_saucer_counter(self, screen):
        text = TextRenderer.render_neon_text(
            self.small_font,
            f"SAUCERS {self.saucers_destroyed}",
            (255, 255, 255),
            (180, 60, 255)
        )
        screen.blit(text, (20, 100))

    def render(self, screen):
        if self.background is not None:
            screen.blit(self.background, (0, 0))
            self.draw_background_overlay(screen)

        score_label = TextRenderer.render_neon_text(
            self.ui_font,
            "SCORE",
            (255, 255, 255),
            (180, 60, 255)
        )
        score_value = TextRenderer.render_neon_text(
            self.ui_font,
            str(self.score),
            (255, 255, 255),
            (180, 60, 255)
        )
        lives_label = TextRenderer.render_neon_text(
            self.ui_font,
            "LIVES",
            (255, 255, 255),
            (180, 60, 255)
        )
        wave_label = TextRenderer.render_neon_text(
            self.small_font,
            f"WAVE {self.wave}/20",
            (255, 255, 255),
            (180, 60, 255)
        )
        hint_label = TextRenderer.render_neon_text(
            self.small_font,
            "A D OR LEFT RIGHT MOVE    HOLD SPACE SHOOT    ESC MENU",
            (255, 255, 255),
            (180, 60, 255)
        )

        screen.blit(score_label, (110, 14))
        screen.blit(score_value, (265, 14))
        screen.blit(lives_label, (WINDOW_WIDTH - 340, 14))
        screen.blit(wave_label, (14, 62))
        screen.blit(hint_label, (20, WINDOW_HEIGHT - 62))

        self.draw_lives(screen)
        self.draw_bottom_line(screen)
        self.draw_double_fire_label(screen)
        self.draw_saucer_counter(screen)

        for bunker in self.bunkers:
            bunker.draw(screen)

        self.player.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        for bullet in self.enemy_bullets:
            bullet.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        if self.saucer is not None:
            self.saucer.draw(screen)

        for explosion in self.explosions:
            explosion.draw(screen)

        self.draw_wave_banner(screen)