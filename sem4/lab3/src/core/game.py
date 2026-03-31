import pygame

import src.core.settings as settings
from src.core.state_manager import StateManager
from src.data.leaderboard_manager import LeaderboardManager
from src.core.sound_manager import SoundManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.base_width = settings.WINDOW_WIDTH
        self.base_height = settings.WINDOW_HEIGHT

        if settings.FULLSCREEN:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.base_width, self.base_height))

        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption(settings.WINDOW_TITLE)

        self.render_surface = pygame.Surface((self.base_width, self.base_height))

        scale_x = self.screen_width / self.base_width
        scale_y = self.screen_height / self.base_height
        self.scale = min(scale_x, scale_y)

        self.scaled_width = int(self.base_width * self.scale)
        self.scaled_height = int(self.base_height * self.scale)

        self.offset_x = (self.screen_width - self.scaled_width) // 2
        self.offset_y = (self.screen_height - self.scaled_height) // 2

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.leaderboard_manager = LeaderboardManager()
        self.sound_manager = SoundManager()

        self.state_manager = StateManager()

        from src.states.menu_state import MenuState
        self.state_manager.set_state(MenuState(self, self.state_manager))

    def quit(self):
        self.is_running = False

    def run(self):
        while self.is_running:
            dt = self.clock.tick(settings.FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.state_manager.handle_event(event)

            self.state_manager.update(dt)

            self.render_surface.fill(settings.BACKGROUND_COLOR)
            self.state_manager.render(self.render_surface)

            scaled_surface = pygame.transform.scale(
                self.render_surface,
                (self.scaled_width, self.scaled_height)
            )

            self.screen.fill((0, 0, 0))
            self.screen.blit(scaled_surface, (self.offset_x, self.offset_y))
            pygame.display.flip()

        pygame.quit()