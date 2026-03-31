import math
import random
import pygame


class WarpRay:
    def __init__(self, center_x, center_y, screen_width, screen_height):
        self.center_x = center_x
        self.center_y = center_y
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.angle = random.uniform(-2.7, 0.2)

        self.distance = random.uniform(4, 20)
        self.speed = random.uniform(4.5, 8.5)
        self.acceleration = random.uniform(22, 42)

        self.base_length = random.uniform(20, 46)
        self.max_extra_length = random.uniform(140, 260)

        self.base_width = random.uniform(2.0, 3.4)
        self.max_extra_width = random.uniform(6.0, 11.0)

        self.life = 1.0

        self.glow_color = random.choice([
            (255, 80, 210),
            (255, 120, 230),
            (255, 170, 245),
        ])
        self.core_color = (255, 255, 255)

    def update(self, dt):
        self.speed += self.acceleration * dt
        self.distance += self.speed * dt

        margin = 260
        x = self.center_x + math.cos(self.angle) * self.distance
        y = self.center_y + math.sin(self.angle) * self.distance

        if (
            x < -margin or x > self.screen_width + margin or
            y < -margin or y > self.screen_height + margin
        ):
            self.life = 0.0

    def is_alive(self):
        return self.life > 0.0

    def draw(self, surface):
        if not self.is_alive():
            return

        growth = min(1.0, self.distance / 520.0)

        length = self.base_length + self.max_extra_length * growth
        width = self.base_width + self.max_extra_width * growth

        ex = self.center_x + math.cos(self.angle) * self.distance
        ey = self.center_y + math.sin(self.angle) * self.distance

        sx = self.center_x + math.cos(self.angle) * max(0, self.distance - length)
        sy = self.center_y + math.sin(self.angle) * max(0, self.distance - length)

        glow_alpha = int(65 + 95 * growth)
        core_alpha = int(145 + 90 * growth)

        line_width = max(2, int(width))
        core_width = max(1, int(width * 0.28))
        pad = line_width + 10

        min_x = int(min(sx, ex)) - pad
        min_y = int(min(sy, ey)) - pad
        max_x = int(max(sx, ex)) + pad
        max_y = int(max(sy, ey)) + pad

        local_w = max(2, max_x - min_x + 1)
        local_h = max(2, max_y - min_y + 1)

        local = pygame.Surface((local_w, local_h), pygame.SRCALPHA)

        lsx = sx - min_x
        lsy = sy - min_y
        lex = ex - min_x
        ley = ey - min_y

        pygame.draw.line(
            local,
            (*self.glow_color, glow_alpha),
            (int(lsx), int(lsy)),
            (int(lex), int(ley)),
            line_width
        )

        pygame.draw.line(
            local,
            (*self.glow_color, min(255, glow_alpha + 35)),
            (int(lsx), int(lsy)),
            (int(lex), int(ley)),
            max(2, line_width - 3)
        )

        pygame.draw.line(
            local,
            (*self.core_color, core_alpha),
            (int(lsx), int(lsy)),
            (int(lex), int(ley)),
            core_width
        )

        surface.blit(local, (min_x, min_y))