import pygame
from create_assets import create_assets

# constants
SCREEN_SIZE = (1000, 800)
TILE_DIMENSION = 70

# assets
tl = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_1.png'), (TILE_DIMENSION, TILE_DIMENSION))
tr = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_3.png'), (TILE_DIMENSION, TILE_DIMENSION))
bl = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_7.png'), (TILE_DIMENSION, TILE_DIMENSION))
br = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_9.png'), (TILE_DIMENSION, TILE_DIMENSION))
le = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_4.png'), (TILE_DIMENSION, TILE_DIMENSION))
re = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_6.png'), (TILE_DIMENSION, TILE_DIMENSION))
te = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_2.png'), (TILE_DIMENSION, TILE_DIMENSION))
be = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_8.png'), (TILE_DIMENSION, TILE_DIMENSION))
ft = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_5.png'), (TILE_DIMENSION, TILE_DIMENSION))
ot = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_5.png'), (TILE_DIMENSION, TILE_DIMENSION))
co = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_1.png'), (TILE_DIMENSION, TILE_DIMENSION))

collideable = [tl, tr, bl, br, le, re, te, be, ot, co]

    # tl - top left
    # tr - top right
    # bl - bottom left
    # br - bottom right
    # le - left edge
    # re - right edge
    # te - top edge
    # be - bottom edge
    # ft - floor tile
    # ot - object tile (copy of floor tile image but collideable)
    # co - chest object

game_map = [
    [tl, te, te, te, tr, tl, te, te, te, te, te, te, tr],
    [le, ft, ft, ft, re, le, ft, ft, ft, ft, ft, ft, re],
    [le, ft, ot, ft, re, le, ft, ft, ft, ft, ft, ft, re],
    [le, ft, ft, ft, re, le, ft, ft, ft, ft, ft, ft, re],
    [le, ft, ft, ft, re, le, ft, ft, ft, ft, ft, ft, re],
    [bl, be, ft, be, br, bl, be, ft, ft, ft, ft, ft, re],
    [tl, te, ft, te, te, te, te, ft, ft, ft, ft, ft, re],
    [le, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, re],
    [le, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, re],
    [le, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, re],
    [bl, be, be, be, be, be, be, be, be, be, be, be, br],
]

assets = [
    ((255, 255, 255), (30, 30), "./assets/player.png"),
    ((0, 0, 0), (800, 600), "./assets/background.png"),
]

# game variables
inputDisabled = False

pygame.init()
create_assets(assets)
player = {
    'sprite': pygame.transform.scale(pygame.image.load("../../assets/wiz.png"), (TILE_DIMENSION, TILE_DIMENSION)),
    'position': pygame.Vector2(8, 8),
    'new_position': pygame.Vector2(8, 8),
}

enemy = {
    'sprite': pygame.transform.scale(pygame.image.load('../../assets/DunEnemy.png'), (TILE_DIMENSION, TILE_DIMENSION)),
    'position': pygame.Vector2(7, 8),
    'new_position': pygame.Vector2(7, 8),
}

# key = {
#     'sprite': pygame.transform.scale(pygame.image.load('./assets/'), (TILE_DIMENSION, TILE_DIMENSION)),
#     'position': pygame.Vector2(7, 8),
# }

chest = {
    'sprite': pygame.transform.scale(pygame.image.load('../../assets/DunEnemy.png'), (TILE_DIMENSION, TILE_DIMENSION)),
    'position': pygame.Vector2(7, 8),
}

background = {
    'sprite': pygame.image.load("./assets/background.png"),
    'position': pygame.Vector2(0, 0)
}
CLOCK = pygame.time.Clock()
DISPLAY_SURF = pygame.display.set_mode(SCREEN_SIZE)


# game functions
def calculate_new_position(add_position):
    new_position = player['position'] + pygame.Vector2(add_position)
    if game_map[int(new_position.y)][int(new_position.x)] in collideable:
        print("Hey I collided")
        print(game_map[int(new_position.y)][int(new_position.x)])
        return player['position']
    # elif len(game_map) - 2 == int(new_position.y):
    #     return player['position']
    else:
        print(new_position)
        print()
        return new_position


def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    if not inputDisabled:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            player['new_position'] = calculate_new_position((1, 0))
        if keys_pressed[pygame.K_LEFT]:
            player['new_position'] = calculate_new_position((-1, 0))
        if keys_pressed[pygame.K_DOWN]:
            player['new_position'] = calculate_new_position((0, 1))
        if keys_pressed[pygame.K_UP]:
            player['new_position'] = calculate_new_position((0, -1))


def update_world():
    global inputDisabled
    if player['position'] != player['new_position']:
        inputDisabled = True
        player['position'] = player['position'] + (player['new_position'] - player['position']).normalize().elementwise()*.1
    else:
        inputDisabled = False


def draw_to_screen():
    DISPLAY_SURF.blit(background['sprite'], background['position'])

    temp_pos = pygame.Vector2(0, 0)
    for row in range(len(game_map)):
        for cel in range(len(game_map[0])):
            DISPLAY_SURF.blit(game_map[row][cel], temp_pos)
            temp_pos = temp_pos + pygame.Vector2(TILE_DIMENSION, 0)
        temp_pos.x = 0
        temp_pos = temp_pos + pygame.Vector2(0, TILE_DIMENSION)
    DISPLAY_SURF.blit(player['sprite'], player['position'].elementwise()*pygame.Vector2(TILE_DIMENSION))
    DISPLAY_SURF.blit(enemy['sprite'], enemy['position'].elementwise()*pygame.Vector2(TILE_DIMENSION))

    pygame.display.update()


def runtest():
    while True:
        handle_input()
        update_world()
        draw_to_screen()

        CLOCK.tick(60)
