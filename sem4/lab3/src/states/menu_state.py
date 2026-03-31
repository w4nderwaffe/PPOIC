from pathlib import Path
import pygame

from src.states.base_state import BaseState
from src.core.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from src.ui.text_renderer import TextRenderer
from src.ui.menu_effects import WarpRay


class MenuState(BaseState):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)

        self.game.sound_manager.play_music("assets/sounds/spaceinvaders1.mpeg")

        self.item_font = TextRenderer.load_font(28)
        self.hint_font = TextRenderer.load_font(18)

        self.items = [
            "START GAME",
            "HELP",
            "LEADERBOARD",
            "EXIT"
        ]
        self.selected_index = 0

        self.logo = self.load_logo()
        self.arcade_left = self.load_arcade_machine(flipped=False)
        self.arcade_right = self.load_arcade_machine(flipped=True)
        self.planet = self.load_planet()

        self.effect_center_x = WINDOW_WIDTH // 2 + 6
        self.effect_center_y = WINDOW_HEIGHT // 2 - 42

        self.rays = []
        self.ray_spawn_timer = 0.0

    def load_logo(self):
        logo_path = Path("assets/images/menu_logo.png")

        if not logo_path.exists():
            return None

        try:
            image = pygame.image.load(str(logo_path)).convert_alpha()

            max_width = 520
            max_height = 220

            width = image.get_width()
            height = image.get_height()

            scale = min(max_width / width, max_height / height)

            new_width = int(width * scale)
            new_height = int(height * scale)

            return pygame.transform.smoothscale(image, (new_width, new_height))
        except pygame.error:
            return None

    def load_arcade_machine(self, flipped=False):
        machine_path = Path("assets/images/arcade_machine.png")

        if not machine_path.exists():
            return None

        try:
            image = pygame.image.load(str(machine_path)).convert_alpha()

            max_width = 240
            max_height = 520

            width = image.get_width()
            height = image.get_height()

            scale = min(max_width / width, max_height / height)

            new_width = int(width * scale)
            new_height = int(height * scale)

            machine = pygame.transform.smoothscale(image, (new_width, new_height))

            if flipped:
                machine = pygame.transform.flip(machine, True, False)

            return machine
        except pygame.error:
            return None

    def load_planet(self):
        planet_path = Path("assets/images/menu_planet.png")

        if not planet_path.exists():
            return None

        try:
            image = pygame.image.load(str(planet_path)).convert_alpha()

            max_width = 760
            max_height = 250

            width = image.get_width()
            height = image.get_height()

            scale = min(max_width / width, max_height / height)

            new_width = int(width * scale)
            new_height = int(height * scale)

            return pygame.transform.smoothscale(image, (new_width, new_height))
        except pygame.error:
            return None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.items)
                self.game.sound_manager.play("menu_move")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.items)
                self.game.sound_manager.play("menu_move")
            elif event.key == pygame.K_RETURN:
                self.activate_selected_item()

    def activate_selected_item(self):
        selected_item = self.items[self.selected_index]

        if selected_item == "START GAME":
            from src.states.play_state import PlayState
            self.state_manager.set_state(PlayState(self.game, self.state_manager))
        elif selected_item == "HELP":
            from src.states.help_state import HelpState
            self.state_manager.set_state(HelpState(self.game, self.state_manager))
        elif selected_item == "LEADERBOARD":
            from src.states.leaderboard_state import LeaderboardState
            self.state_manager.set_state(LeaderboardState(self.game, self.state_manager))
        elif selected_item == "EXIT":
            self.game.quit()

    def update(self, dt):
        self.update_effects(dt)

    def update_effects(self, dt):
        self.ray_spawn_timer += dt

        while self.ray_spawn_timer >= 0.114:
            self.ray_spawn_timer -= 0.114
            self.rays.append(
                WarpRay(
                    self.effect_center_x,
                    self.effect_center_y,
                    WINDOW_WIDTH,
                    WINDOW_HEIGHT
                )
            )

        for ray in self.rays:
            ray.update(dt)

        self.rays = [ray for ray in self.rays if ray.is_alive()]

    def draw_background_glow(self, screen):
        glow_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        for radius, alpha in [(320, 8), (255, 16), (205, 28), (155, 40), (110, 56)]:
            pygame.draw.circle(
                glow_surface,
                (255, 0, 170, alpha),
                (self.effect_center_x, self.effect_center_y),
                radius
            )

        pygame.draw.circle(
            glow_surface,
            (255, 255, 255, 12),
            (self.effect_center_x, self.effect_center_y),
            78
        )

        screen.blit(glow_surface, (0, 0))

    def draw_floor_glow(self, screen):
        floor_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        pygame.draw.ellipse(
            floor_surface,
            (255, 0, 170, 42),
            pygame.Rect(WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT - 175, 600, 170)
        )
        pygame.draw.ellipse(
            floor_surface,
            (255, 100, 220, 26),
            pygame.Rect(WINDOW_WIDTH // 2 - 230, WINDOW_HEIGHT - 145, 460, 120)
        )

        screen.blit(floor_surface, (0, 0))

    def draw_effects(self, screen):
        for ray in self.rays:
            ray.draw(screen)

    def render(self, screen):
        self.draw_background_glow(screen)
        self.draw_effects(screen)

        if self.planet is not None:
            planet_rect = self.planet.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT + 18))
            screen.blit(self.planet, planet_rect)

        self.draw_floor_glow(screen)

        if self.arcade_left is not None:
            left_rect = self.arcade_left.get_rect(midleft=(35, WINDOW_HEIGHT // 2 + 45))
            screen.blit(self.arcade_left, left_rect)

        if self.arcade_right is not None:
            right_rect = self.arcade_right.get_rect(midright=(WINDOW_WIDTH - 35, WINDOW_HEIGHT // 2 + 45))
            screen.blit(self.arcade_right, right_rect)

        if self.logo is not None:
            logo_rect = self.logo.get_rect(center=(WINDOW_WIDTH // 2, 170))
            screen.blit(self.logo, logo_rect)

        start_y = 365
        spacing = 72

        for index, item in enumerate(self.items):
            if index == self.selected_index:
                text_surface = TextRenderer.render_neon_text(
                    self.item_font,
                    item,
                    (255, 255, 255),
                    (255, 0, 180)
                )
            else:
                text_surface = TextRenderer.render_neon_text(
                    self.item_font,
                    item,
                    (235, 235, 235),
                    (0, 180, 255)
                )

            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, start_y + index * spacing))
            screen.blit(text_surface, text_rect)

        hint_surface = TextRenderer.render_neon_text(
            self.hint_font,
            "UP DOWN OR W S SELECT    ENTER CONFIRM",
            (220, 220, 220),
            (0, 200, 255)
        )
        hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 72))
        screen.blit(hint_surface, hint_rect)