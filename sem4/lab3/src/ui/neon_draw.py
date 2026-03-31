import pygame


def draw_glow_rect(surface, rect, color, glow_color=None, glow_size=8, border_radius=0):
    if glow_color is None:
        glow_color = color

    pad = max(2, glow_size)
    local_w = rect.width + pad * 2
    local_h = rect.height + pad * 2

    local = pygame.Surface((local_w, local_h), pygame.SRCALPHA)

    for expand, alpha in ((pad, 26), (max(1, pad - 3), 40), (max(1, pad - 5), 58)):
        glow_rect = pygame.Rect(
            pad - expand,
            pad - expand,
            rect.width + expand * 2,
            rect.height + expand * 2
        )
        pygame.draw.rect(local, (*glow_color, alpha), glow_rect, border_radius=border_radius)

    body_rect = pygame.Rect(pad, pad, rect.width, rect.height)
    pygame.draw.rect(local, color, body_rect, border_radius=border_radius)

    surface.blit(local, (rect.x - pad, rect.y - pad))


def draw_glow_line(surface, start_pos, end_pos, color, width=3, glow_color=None):
    if glow_color is None:
        glow_color = color

    min_x = min(start_pos[0], end_pos[0])
    min_y = min(start_pos[1], end_pos[1])
    max_x = max(start_pos[0], end_pos[0])
    max_y = max(start_pos[1], end_pos[1])

    pad = width + 10

    local_w = int(max_x - min_x + pad * 2 + 2)
    local_h = int(max_y - min_y + pad * 2 + 2)

    local = pygame.Surface((local_w, local_h), pygame.SRCALPHA)

    sx = start_pos[0] - min_x + pad
    sy = start_pos[1] - min_y + pad
    ex = end_pos[0] - min_x + pad
    ey = end_pos[1] - min_y + pad

    pygame.draw.line(local, (*glow_color, 44), (sx, sy), (ex, ey), width + 8)
    pygame.draw.line(local, (*glow_color, 76), (sx, sy), (ex, ey), width + 4)
    pygame.draw.line(local, color, (sx, sy), (ex, ey), width)

    surface.blit(local, (min_x - pad, min_y - pad))


def draw_glow_circle(surface, center, radius, color, glow_color=None, width=0):
    if glow_color is None:
        glow_color = color

    pad = 12
    local_size = (radius + pad) * 2 + 2
    local = pygame.Surface((local_size, local_size), pygame.SRCALPHA)

    local_center = (local_size // 2, local_size // 2)

    pygame.draw.circle(local, (*glow_color, 34), local_center, radius + 10, 0 if width == 0 else width + 8)
    pygame.draw.circle(local, (*glow_color, 56), local_center, radius + 5, 0 if width == 0 else width + 4)
    pygame.draw.circle(local, color, local_center, radius, width)

    surface.blit(local, (center[0] - local_center[0], center[1] - local_center[1]))


def draw_glow_pixel_pattern(surface, rect, pattern, color, glow_color=None):
    if glow_color is None:
        glow_color = color

    pattern_width = len(pattern[0])
    pattern_height = len(pattern)

    cell_w = max(1, rect.width // pattern_width)
    cell_h = max(1, rect.height // pattern_height)

    pad = 3
    local_w = rect.width + pad * 2
    local_h = rect.height + pad * 2

    local = pygame.Surface((local_w, local_h), pygame.SRCALPHA)

    for row_index, row in enumerate(pattern):
        for col_index, cell in enumerate(row):
            if cell == "1":
                x = pad + col_index * cell_w
                y = pad + row_index * cell_h

                glow_rect = pygame.Rect(x - 1, y - 1, cell_w + 2, cell_h + 2)
                pixel_rect = pygame.Rect(x, y, cell_w, cell_h)

                pygame.draw.rect(local, (*glow_color, 42), glow_rect)
                pygame.draw.rect(local, color, pixel_rect)

    surface.blit(local, (rect.x - pad, rect.y - pad))