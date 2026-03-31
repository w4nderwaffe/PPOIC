import pygame

from src.states.base_state import BaseState
from src.core.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from src.ui.text_renderer import TextRenderer


class LeaderboardState(BaseState):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)

        self.game.sound_manager.play_music("assets/sounds/spaceinvaders1.mpeg")

        self.title_font = TextRenderer.load_font(48)
        self.text_font = TextRenderer.load_font(28)
        self.small_font = TextRenderer.load_font(22)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from src.states.menu_state import MenuState
            self.state_manager.set_state(MenuState(self.game, self.state_manager))

    def update(self, dt):
        pass

    def render(self, screen):
        title_surface = TextRenderer.render_neon_text(
            self.title_font,
            "LEADERBOARD",
            (255, 255, 255),
            (180, 60, 255)
        )
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 90))
        screen.blit(title_surface, title_rect)

        records = self.game.leaderboard_manager.get_records()

        header_rank = TextRenderer.render_neon_text(self.text_font, "RANK", (255, 255, 255), (180, 60, 255))
        header_name = TextRenderer.render_neon_text(self.text_font, "NAME", (255, 255, 255), (180, 60, 255))
        header_score = TextRenderer.render_neon_text(self.text_font, "SCORE", (255, 255, 255), (180, 60, 255))

        screen.blit(header_rank, (150, 150))
        screen.blit(header_name, (330, 150))
        screen.blit(header_score, (610, 150))

        start_y = 230
        row_height = 42

        if not records:
            empty_surface = TextRenderer.render_neon_text(
                self.text_font,
                "NO RECORDS YET",
                (255, 255, 255),
                (180, 60, 255)
            )
            empty_rect = empty_surface.get_rect(center=(WINDOW_WIDTH // 2, 320))
            screen.blit(empty_surface, empty_rect)
        else:
            for index, record in enumerate(records, start=1):
                y = start_y + (index - 1) * row_height

                rank_surface = TextRenderer.render_neon_text(
                    self.text_font,
                    str(index),
                    (255, 255, 255),
                    (180, 60, 255)
                )
                name_surface = TextRenderer.render_neon_text(
                    self.text_font,
                    record["name"],
                    (255, 255, 255),
                    (180, 60, 255)
                )
                score_surface = TextRenderer.render_neon_text(
                    self.text_font,
                    str(record["score"]),
                    (255, 255, 255),
                    (180, 60, 255)
                )

                screen.blit(rank_surface, (175, y))
                screen.blit(name_surface, (330, y))
                screen.blit(score_surface, (640, y))

        hint_surface = TextRenderer.render_neon_text(
            self.small_font,
            "PRESS ESC TO RETURN TO MENU",
            (255, 255, 255),
            (180, 60, 255)
        )
        hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70))
        screen.blit(hint_surface, hint_rect)