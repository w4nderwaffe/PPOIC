import random
import pygame

from src.core.settings import (
    WINDOW_WIDTH,
    SAUCER_WIDTH,
    SAUCER_HEIGHT,
    SAUCER_SPEED,
    SAUCER_Y,
    SAUCER_SCORE
)


class Saucer:
    PATTERN = [
        "000111111110000",
        "001111111111000",
        "011001001001100",
        "111111111111110",
        "111111111111110",
        "001100110011000",
        "000110000110000",
    ]

    def __init__(self):
        self.direction = random.choice([-1, 1])

        if self.direction == 1:
            x = -SAUCER_WIDTH
        else:
            x = WINDOW_WIDTH + SAUCER_WIDTH

        self.rect = pygame.Rect(x, SAUCER_Y, SAUCER_WIDTH, SAUCER_HEIGHT)
        self.speed = SAUCER_SPEED
        self.is_active = True
        self.score_value = SAUCER_SCORE
        self.color = (255, 90, 90)
        self.glow_color = (255, 40, 40)

        self.sprite = self.build_sprite()

    def build_sprite(self):
        pattern_width = len(self.PATTERN[0])
        pattern_height = len(self.PATTERN)

        cell_w = max(1, self.rect.width // pattern_width)
        cell_h = max(1, self.rect.height // pattern_height)

        pad = 3
        sprite = pygame.Surface((self.rect.width + pad * 2, self.rect.height + pad * 2), pygame.SRCALPHA)

        for row_index, row in enumerate(self.PATTERN):
            for col_index, cell in enumerate(row):
                if cell == "1":
                    x = pad + col_index * cell_w
                    y = pad + row_index * cell_h

                    glow_rect = pygame.Rect(x - 1, y - 1, cell_w + 2, cell_h + 2)
                    pixel_rect = pygame.Rect(x, y, cell_w, cell_h)

                    pygame.draw.rect(sprite, (*self.glow_color, 42), glow_rect)
                    pygame.draw.rect(sprite, self.color, pixel_rect)

        return sprite

    def update(self, dt):
        self.rect.x += int(self.direction * self.speed * dt)

        if self.direction == 1 and self.rect.left > WINDOW_WIDTH:
            self.is_active = False
        elif self.direction == -1 and self.rect.right < 0:
            self.is_active = False

    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x - 3, self.rect.y - 3))