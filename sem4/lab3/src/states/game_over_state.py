import pygame

from src.states.base_state import BaseState
from src.core.settings import WINDOW_WIDTH, WINDOW_HEIGHT, TEXT_COLOR, ACCENT_COLOR


class GameOverState(BaseState):
    def __init__(self, game, state_manager, score=0):
        super().__init__(game, state_manager)

        self.score = score
        self.title_font = pygame.font.SysFont("courier", 52, bold=True)
        self.text_font = pygame.font.SysFont("courier", 28, bold=True)
        self.small_font = pygame.font.SysFont("courier", 22, bold=True)

        self.is_first_place = self.game.leaderboard_manager.is_first_place(self.score)
        self.name_input = ""
        self.saved = False

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.is_first_place and not self.saved:
            if event.key == pygame.K_RETURN:
                self.save_record_and_go_to_leaderboard()
            elif event.key == pygame.K_BACKSPACE:
                self.name_input = self.name_input[:-1]
            elif event.key == pygame.K_ESCAPE:
                from src.states.menu_state import MenuState
                self.state_manager.set_state(MenuState(self.game, self.state_manager))
            else:
                if event.unicode and event.unicode.isprintable() and len(self.name_input) < 12:
                    self.name_input += event.unicode.upper()
        else:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                from src.states.menu_state import MenuState
                self.state_manager.set_state(MenuState(self.game, self.state_manager))

    def save_record_and_go_to_leaderboard(self):
        name = self.name_input.strip()
        if not name:
            name = "PLAYER"

        self.game.leaderboard_manager.add_record(name, self.score)
        self.saved = True

        from src.states.leaderboard_state import LeaderboardState
        self.state_manager.set_state(LeaderboardState(self.game, self.state_manager))

    def update(self, dt):
        pass

    def render(self, screen):
        title_surface = self.title_font.render("GAME OVER", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 120))
        screen.blit(title_surface, title_rect)

        score_surface = self.text_font.render(f"SCORE {self.score}", True, ACCENT_COLOR)
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, 210))
        screen.blit(score_surface, score_rect)

        if self.is_first_place:
            congrats_surface = self.text_font.render("CONGRATULATIONS! NEW TOP SCORE!", True, ACCENT_COLOR)
            congrats_rect = congrats_surface.get_rect(center=(WINDOW_WIDTH // 2, 300))
            screen.blit(congrats_surface, congrats_rect)

            prompt_surface = self.text_font.render("ENTER YOUR NAME:", True, TEXT_COLOR)
            prompt_rect = prompt_surface.get_rect(center=(WINDOW_WIDTH // 2, 380))
            screen.blit(prompt_surface, prompt_rect)

            input_text = self.name_input if self.name_input else "_"
            input_surface = self.title_font.render(input_text, True, TEXT_COLOR)
            input_rect = input_surface.get_rect(center=(WINDOW_WIDTH // 2, 455))
            screen.blit(input_surface, input_rect)

            hint_surface = self.small_font.render("TYPE NAME AND PRESS ENTER TO SAVE", True, TEXT_COLOR)
            hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, 550))
            screen.blit(hint_surface, hint_rect)

            esc_surface = self.small_font.render("PRESS ESC TO RETURN TO MENU", True, TEXT_COLOR)
            esc_rect = esc_surface.get_rect(center=(WINDOW_WIDTH // 2, 590))
            screen.blit(esc_surface, esc_rect)
        else:
            hint_surface = self.text_font.render("PRESS ENTER OR ESC TO RETURN", True, TEXT_COLOR)
            hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, 380))
            screen.blit(hint_surface, hint_rect)