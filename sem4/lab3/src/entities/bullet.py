import pygame

from src.core.settings import BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED
from src.ui.neon_draw import draw_glow_rect


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(
            x - BULLET_WIDTH // 2,
            y - BULLET_HEIGHT,
            BULLET_WIDTH,
            BULLET_HEIGHT
        )
        self.speed = BULLET_SPEED
        self.is_active = True
        self.color = (255, 180, 255)
        self.glow_color = (180, 60, 255)

    def update(self, dt):
        self.rect.y -= int(self.speed * dt)
        if self.rect.bottom < 0:
            self.is_active = False

    def draw(self, screen):
        draw_glow_rect(screen, self.rect, self.color, self.glow_color)