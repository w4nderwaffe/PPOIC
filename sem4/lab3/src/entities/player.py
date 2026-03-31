import pygame

from src.core.settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SPEED
)
from src.ui.neon_draw import draw_glow_rect


class Player:
    def __init__(self):
        self.rect = pygame.Rect(
            WINDOW_WIDTH // 2 - PLAYER_WIDTH // 2,
            WINDOW_HEIGHT - 95,
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )
        self.speed = PLAYER_SPEED
        self.base_color = (255, 150, 255)
        self.glow_color = (180, 60, 255)

    def update(self, dt, move_left, move_right):
        dx = 0

        if move_left:
            dx -= self.speed * dt
        if move_right:
            dx += self.speed * dt

        self.rect.x += int(dx)

        if self.rect.left < 20:
            self.rect.left = 20
        if self.rect.right > WINDOW_WIDTH - 20:
            self.rect.right = WINDOW_WIDTH - 20

    def get_bullet_spawn_position(self):
        return self.rect.centerx, self.rect.top

    def draw(self, screen):
        body_rect = pygame.Rect(self.rect.x, self.rect.y + 12, self.rect.width, self.rect.height - 12)
        turret_rect = pygame.Rect(self.rect.centerx - 5, self.rect.y, 10, 14)

        draw_glow_rect(screen, body_rect, self.base_color, self.glow_color)
        draw_glow_rect(screen, turret_rect, self.base_color, self.glow_color)