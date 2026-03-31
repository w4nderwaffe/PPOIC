import pygame

from src.states.base_state import BaseState
from src.core.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from src.entities.enemy import Enemy
from src.entities.saucer import Saucer
from src.data.config_loader import ConfigLoader
from src.ui.text_renderer import TextRenderer


class HelpState(BaseState):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)

        self.game.sound_manager.play_music("assets/sounds/spaceinvaders1.mpeg")

        self.title_font = TextRenderer.load_font(42)
        self.text_font = TextRenderer.load_font(20)
        self.small_font = TextRenderer.load_font(16)

        enemies_data = ConfigLoader.load_json("config/enemies.json")
        self.enemy_configs = {item["id"]: item for item in enemies_data["types"]}

        self.enemy_samples = []
        start_x_left = 90
        start_x_right = 490
        start_y = 150
        row_gap = 66

        for enemy_type in range(5):
            enemy = Enemy(start_x_left, start_y + enemy_type * row_gap, enemy_type, self.enemy_configs[enemy_type], 0)
            self.enemy_samples.append(enemy)

        for enemy_type in range(5, 10):
            enemy = Enemy(start_x_right, start_y + (enemy_type - 5) * row_gap, enemy_type, self.enemy_configs[enemy_type], 0)
            self.enemy_samples.append(enemy)

        self.saucer = Saucer()
        self.saucer.rect.x = 390
        self.saucer.rect.y = 510

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from src.states.menu_state import MenuState
            self.state_manager.set_state(MenuState(self.game, self.state_manager))

    def update(self, dt):
        for enemy in self.enemy_samples:
            enemy.update(dt)

    def render(self, screen):
        title_surface = TextRenderer.render_neon_text(
            self.title_font,
            "HELP / ENEMIES",
            (255, 255, 255),
            (180, 60, 255)
        )
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 55))
        screen.blit(title_surface, title_rect)

        controls_surface = TextRenderer.render_neon_text(
            self.small_font,
            "MOVE A D OR LEFT RIGHT    SHOOT SPACE    MENU ESC",
            (255, 255, 255),
            (180, 60, 255)
        )
        controls_rect = controls_surface.get_rect(center=(WINDOW_WIDTH // 2, 95))
        screen.blit(controls_surface, controls_rect)

        for enemy in self.enemy_samples:
            enemy.draw(screen)

        for enemy_type in range(5):
            enemy = self.enemy_samples[enemy_type]
            text = TextRenderer.render_neon_text(
                self.text_font,
                f"{enemy.get_name()}  {enemy.get_score()} PTS  HP {enemy.hp}",
                (255, 255, 255),
                (180, 60, 255)
            )
            screen.blit(text, (150, enemy.rect.y + 2))

        for enemy_type in range(5, 10):
            enemy = self.enemy_samples[enemy_type]
            text = TextRenderer.render_neon_text(
                self.text_font,
                f"{enemy.get_name()}  {enemy.get_score()} PTS  HP {enemy.hp}",
                (255, 255, 255),
                (180, 60, 255)
            )
            screen.blit(text, (550, enemy.rect.y + 2))

        self.saucer.draw(screen)

        saucer_text = TextRenderer.render_neon_text(
            self.text_font,
            "RED SAUCER  300 PTS",
            (255, 255, 255),
            (255, 80, 80)
        )
        saucer_rect = saucer_text.get_rect(center=(WINDOW_WIDTH // 2, 548))
        screen.blit(saucer_text, saucer_rect)

        tip1 = TextRenderer.render_neon_text(
            self.small_font,
            "ALL 10 ENEMY TYPES ARE LOADED FROM CONFIG AND HAVE UNIQUE PARAMETERS",
            (255, 255, 255),
            (180, 60, 255)
        )
        tip2 = TextRenderer.render_neon_text(
            self.small_font,
            "DESTROY 2 RED SAUCERS TO ACTIVATE SECRET DOUBLE RAPID FIRE FOR 4 SECONDS",
            (255, 255, 255),
            (180, 60, 255)
        )
        tip3 = TextRenderer.render_neon_text(
            self.small_font,
            "PRESS ESC TO RETURN TO MENU",
            (255, 255, 255),
            (180, 60, 255)
        )

        tip1_rect = tip1.get_rect(center=(WINDOW_WIDTH // 2, 610))
        tip2_rect = tip2.get_rect(center=(WINDOW_WIDTH // 2, 638))
        tip3_rect = tip3.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 24))

        screen.blit(tip1, tip1_rect)
        screen.blit(tip2, tip2_rect)
        screen.blit(tip3, tip3_rect)