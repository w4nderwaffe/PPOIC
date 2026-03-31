import pygame

from src.core.settings import ENEMY_WIDTH, ENEMY_HEIGHT
from src.ui.neon_draw import draw_glow_rect


class Enemy:
    def __init__(self, x, y, enemy_type, config, column=0):
        self.enemy_type = enemy_type
        self.column = column
        self.config = config
        self.hp = self.config["hp"]
        self.is_alive = True

        self.anchor_x = x
        self.anchor_y = y
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

        self.color = (120, 255, 120)
        self.glow_color = (0, 255, 90)

        self.sprite = self.build_sprite(self.config["pattern"])

    def build_sprite(self, pattern):
        pattern_width = len(pattern[0])
        pattern_height = len(pattern)

        cell_w = max(1, self.rect.width // pattern_width)
        cell_h = max(1, self.rect.height // pattern_height)

        sprite_w = pattern_width * cell_w + 6
        sprite_h = pattern_height * cell_h + 6
        sprite = pygame.Surface((sprite_w, sprite_h), pygame.SRCALPHA)

        for row_index, row in enumerate(pattern):
            for col_index, cell in enumerate(row):
                if cell != "1":
                    continue

                x = 3 + col_index * cell_w
                y = 3 + row_index * cell_h

                glow_rect = pygame.Rect(x - 1, y - 1, cell_w + 2, cell_h + 2)
                pixel_rect = pygame.Rect(x, y, cell_w, cell_h)

                pygame.draw.rect(sprite, (*self.glow_color, 36), glow_rect)
                pygame.draw.rect(sprite, self.color, pixel_rect)

        return sprite

    def move_horizontal(self, dx):
        self.anchor_x += dx
        self.rect.x = self.anchor_x
        self.rect.y = self.anchor_y

    def move_down(self, dy):
        self.anchor_y += dy
        self.rect.x = self.anchor_x
        self.rect.y = self.anchor_y

    def update(self, dt):
        self.rect.x = self.anchor_x
        self.rect.y = self.anchor_y

    def get_bullet_spawn_position(self):
        return self.rect.centerx, self.rect.bottom

    def get_score(self):
        return self.config["score"]

    def get_fire_weight(self):
        return self.config["fire_weight"]

    def get_name(self):
        return self.config["name"]

    def take_hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.is_alive = False
            return True
        return False

    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x - 3, self.rect.y - 3))

        if self.hp > 1:
            hp_rect = pygame.Rect(self.rect.x, self.rect.y - 6, self.hp * 10, 4)
            draw_glow_rect(screen, hp_rect, self.color, self.glow_color, glow_size=5)