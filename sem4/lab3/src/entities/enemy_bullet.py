import pygame

from src.core.settings import ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT, ENEMY_BULLET_SPEED, ENEMY_BULLET_COLOR, WINDOW_HEIGHT


class EnemyBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT)
        self.rect.midtop = (x, y)
        self.speed = ENEMY_BULLET_SPEED
        self.color = ENEMY_BULLET_COLOR
        self.is_active = True

    def update(self, dt):
        self.rect.y += int(self.speed * dt)

        if self.rect.top > WINDOW_HEIGHT:
            self.is_active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)