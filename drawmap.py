import pygame
from variable import *

def draw_grid(screen, grid, cell_size, visited=None, path=None):
    # Define colors for predefined and unknown characters
    colors = {
        '0': WHITE,
        '-1': GRAY,
        'S': GREEN,
        'G': RED
    }
    
    # Define font
    font = pygame.font.Font(None, cell_size // 2)  # Font size is half the cell size
    
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell in colors:
                color = colors[cell]
            else:
                color = BLUE  # Color for unknown characters

            # Draw the cell
            pygame.draw.rect(screen, color, pygame.Rect(col_idx * cell_size, row_idx * cell_size, cell_size, cell_size))
            # Draw the border
            pygame.draw.rect(screen, BLACK, pygame.Rect(col_idx * cell_size, row_idx * cell_size, cell_size, cell_size), 1)

            if cell not in ['-1', '0']:
                # Draw text
                text_surface = font.render(cell, True, BLACK)
                text_rect = text_surface.get_rect(center=(col_idx * cell_size + cell_size // 2, row_idx * cell_size + cell_size // 2))
                screen.blit(text_surface, text_rect)

    if visited:
        for (r, c) in visited:
            if grid[r][c] not in ['S', 'G']:
                pygame.draw.rect(screen, SEARCH_COLOR, pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, BLACK, pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size), 1)

    if path:
        for i in range(len(path) - 1):
            start_pos = (path[i][1] * cell_size + cell_size // 2, path[i][0] * cell_size + cell_size // 2)
            end_pos = (path[i + 1][1] * cell_size + cell_size // 2, path[i + 1][0] * cell_size + cell_size // 2)
            pygame.draw.line(screen, PATH_COLOR, start_pos, end_pos, 3)
