import pygame

from src.core.settings import BUNKER_BLOCK_SIZE
from src.ui.neon_draw import draw_glow_rect


class BunkerBlock:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.is_alive = True


class Bunker:
    PATTERN = [
        "00111100",
        "01111110",
        "11111111",
        "11100111",
        "11000011",
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocks = []
        self.base_color = (255, 150, 255)
        self.glow_color = (180, 60, 255)
        self.create_blocks()

    def create_blocks(self):
        self.blocks = []

        for row_index, row in enumerate(self.PATTERN):
            for col_index, cell in enumerate(row):
                if cell == "1":
                    block_x = self.x + col_index * BUNKER_BLOCK_SIZE
                    block_y = self.y + row_index * BUNKER_BLOCK_SIZE
                    self.blocks.append(BunkerBlock(block_x, block_y, BUNKER_BLOCK_SIZE))

    def get_alive_blocks(self):
        return [block for block in self.blocks if block.is_alive]

    def draw(self, screen):
        for block in self.blocks:
            if block.is_alive:
                draw_glow_rect(screen, block.rect, self.base_color, self.glow_color)