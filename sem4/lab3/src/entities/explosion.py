import pygame

from src.core.settings import ACCENT_COLOR, TEXT_COLOR


class Explosion:
    def __init__(self, x, y, duration, max_radius):
        self.x = x
        self.y = y
        self.duration = duration
        self.max_radius = max_radius
        self.elapsed = 0.0
        self.is_active = True

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.is_active = False

    def draw(self, screen):
        if not self.is_active:
            return

        progress = self.elapsed / self.duration
        if progress > 1:
            progress = 1

        outer_radius = max(2, int(self.max_radius * progress))
        inner_radius = max(1, int(outer_radius * 0.55))

        pygame.draw.circle(screen, TEXT_COLOR, (self.x, self.y), outer_radius, 2)
        pygame.draw.circle(screen, ACCENT_COLOR, (self.x, self.y), inner_radius, 2)

        line_size = max(4, int(self.max_radius * (1 - progress) + 4))
        pygame.draw.line(screen, TEXT_COLOR, (self.x - line_size, self.y), (self.x + line_size, self.y), 2)
        pygame.draw.line(screen, TEXT_COLOR, (self.x, self.y - line_size), (self.x, self.y + line_size), 2)