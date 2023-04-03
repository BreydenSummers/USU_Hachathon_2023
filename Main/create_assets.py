import pygame

def square_creator(color, size, file_name):
    # color is Color, size is tuple
    temp_surface = pygame.Surface(size)
    temp_surface.fill(color)
    pygame.image.save(temp_surface, file_name)
    print(color, size, file_name, temp_surface)

def create_assets(assets):
    for asset in assets:
        square_creator(asset[0], asset[1], asset[2])
