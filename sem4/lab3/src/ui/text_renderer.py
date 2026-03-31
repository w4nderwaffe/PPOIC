from pathlib import Path
import pygame


class TextRenderer:
    FONT_PATH = "assets/fonts/arcade.ttf"

    @staticmethod
    def load_font(size: int) -> pygame.font.Font:
        font_path = Path(TextRenderer.FONT_PATH)

        if font_path.exists():
            return pygame.font.Font(str(font_path), size)

        return pygame.font.SysFont("courier", size, bold=True)

    @staticmethod
    def render_neon_text(
        font: pygame.font.Font,
        text: str,
        base_color: tuple[int, int, int],
        glow_color: tuple[int, int, int],
    ) -> pygame.Surface:
        base = font.render(text, True, base_color)

        glow_far = font.render(text, True, glow_color)
        glow_mid = font.render(text, True, glow_color)
        glow_near = font.render(text, True, glow_color)

        width = base.get_width() + 20
        height = base.get_height() + 20

        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        glow_far.set_alpha(45)
        glow_mid.set_alpha(80)
        glow_near.set_alpha(140)

        far_offsets = [
            (-4, 0), (4, 0), (0, -4), (0, 4),
            (-3, -3), (3, -3), (-3, 3), (3, 3),
        ]

        mid_offsets = [
            (-2, 0), (2, 0), (0, -2), (0, 2),
            (-2, -2), (2, -2), (-2, 2), (2, 2),
        ]

        near_offsets = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
        ]

        center_x = 10
        center_y = 10

        for dx, dy in far_offsets:
            surface.blit(glow_far, (center_x + dx, center_y + dy))

        for dx, dy in mid_offsets:
            surface.blit(glow_mid, (center_x + dx, center_y + dy))

        for dx, dy in near_offsets:
            surface.blit(glow_near, (center_x + dx, center_y + dy))

        surface.blit(base, (center_x, center_y))
        return surface