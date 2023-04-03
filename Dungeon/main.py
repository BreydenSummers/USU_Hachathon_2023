import pygame
import random
from Dungeon.create_assets import create_assets
import os

def dungeonGame(programDir):
    # constants
    TILE_DIMENSION = 70
    SCREEN_SIZE = (13*TILE_DIMENSION, 11*TILE_DIMENSION)

    currentDir = os.getcwd()
    os.chdir(programDir)

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
    gt = pygame.transform.scale(pygame.image.load('../assets/DungeonSheet_5.png'), (TILE_DIMENSION, TILE_DIMENSION))

    collideable = [tl, tr, bl, br, le, re, te, be, ot]

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

    game_map = [
        [tl, te, te, te, tr, tl, te, te, te, te, te, te, tr],
        [le, ft, ft, ft, re, le, ft, ft, ft, ft, ft, ft, re],
        [le, ft, ft, ft, re, le, ft, ft, ft, ft, ft, ft, re],
        [le, ft, ft, ft, re, le, ft, ft, ft, ft, ft, ft, re],
        [le, ft, ft, ft, re, le, ft, ft, ft, ft, ft, ft, re],
        [bl, be, ot, be, br, bl, be, ft, ft, ft, ft, ft, re],
        [tl, te, ft, te, te, te, te, ft, ft, ft, ft, ft, re],
        [le, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, re],
        [le, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, re],
        [le, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, re],
        [bl, be, be, be, be, be, be, be, be, be, be, be, br],
    ]

    assets = [
        ((255, 255, 255), (30, 30), "./assets/player.png"),
        ((0, 0, 0), (800, 600), "./assets/background.png"),
        ((255, 0, 0), (TILE_DIMENSION, TILE_DIMENSION), "./assets/tilextile_red.png"),
    ]

    # game variables
    inputDisabled = False
    game_won = False
    game_lost = False

    possible_movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    pygame.init()
    change_animation = pygame.event.custom_type()
    move_enemy = pygame.event.custom_type()
    pygame.time.set_timer(move_enemy, 2000)
    pygame.time.set_timer(change_animation, 400)
    animation_frame = 0
    create_assets(assets)
    debug_square = pygame.image.load('./assets/tilextile_red.png')
    player = {
        'sprite': pygame.transform.scale(pygame.image.load("../assets/wiz.png"), (TILE_DIMENSION, TILE_DIMENSION)),
        'position': pygame.Vector2(8, 8),
        'new_position': pygame.Vector2(8, 8),
        'moving_left': False,
    }

    enemies = []
    enemies_positions = [
        pygame.Vector2(10, 3),
        pygame.Vector2(8, 4),
        pygame.Vector2(11, 5),
        pygame.Vector2(2, 7),
        pygame.Vector2(5, 8),
    ]
    for i in range(len(enemies_positions)):
        enemies.append(
            {
                'sprite':
                    [
                        pygame.transform.scale(pygame.image.load('../assets/clank/ClankGIF-1.png'),
                                               (TILE_DIMENSION, TILE_DIMENSION)),
                        pygame.transform.scale(pygame.image.load('../assets/clank/ClankGIF-2.png'),
                                               (TILE_DIMENSION, TILE_DIMENSION)),
                    ],
                'position': enemies_positions[i],
                'new_position': enemies_positions[i],
            }
        )

    key = {
        'sprite': pygame.transform.scale(pygame.image.load('../assets/Key.png'), (TILE_DIMENSION, TILE_DIMENSION)),
        'position': pygame.Vector2(10, 3),
        'collected': False
    }

    chest = {
        'sprite': pygame.transform.scale(pygame.image.load('../assets/Chest(1).png'), (TILE_DIMENSION, TILE_DIMENSION)),
        'position': pygame.Vector2(2, 2),
    }

    door = {
        'sprite': pygame.transform.scale(pygame.image.load('../assets/Door.png'), (TILE_DIMENSION, TILE_DIMENSION)),
        'position': pygame.Vector2(2, 5),
    }

    background = {
        'sprite': pygame.image.load("./assets/background.png"),
        'position': pygame.Vector2(0, 0)
    }
    CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode(SCREEN_SIZE)


    # game functions
    def calculate_new_position(add_position, mover):
        new_position = mover['position'] + pygame.Vector2(add_position)
        if game_map[int(new_position.y)][int(new_position.x)] in collideable:
            return mover['position']
        else:
            print(new_position)
            return new_position


    def handle_input():
        nonlocal game_won
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                game_won = True
            if event.type == change_animation:
                nonlocal animation_frame
                animation_frame = animation_frame + 1
            if event.type == move_enemy:
                for enemy in enemies:
                    while enemy['position'] == enemy['new_position']:
                        enemy['new_position'] = calculate_new_position(random.choice(possible_movements), enemy)

        if not inputDisabled:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RIGHT]:
                player['new_position'] = calculate_new_position((1, 0), player)
                if player['moving_left']:
                    player['sprite'] = pygame.transform.flip(player['sprite'], 1, 0)
                    player['moving_left'] = False
            if keys_pressed[pygame.K_LEFT]:
                player['new_position'] = calculate_new_position((-1, 0), player)
                if not player['moving_left']:
                    player['sprite'] = pygame.transform.flip(player['sprite'], 1, 0)
                    player['moving_left'] = True
            if keys_pressed[pygame.K_DOWN]:
                player['new_position'] = calculate_new_position((0, 1), player)
            if keys_pressed[pygame.K_UP]:
                player['new_position'] = calculate_new_position((0, -1), player)


    def update_world():
        nonlocal inputDisabled
        if player['position'] != player['new_position']:
            inputDisabled = True
            player['position'] = player['position'] + (player['new_position'] - player['position']).normalize().elementwise()*.1
        else:
            inputDisabled = False

        for enemy in enemies:
            if player['position'] == enemy['position']:
                nonlocal game_lost
                game_lost = True
            if enemy['position'] != enemy['new_position']:
                enemy['position'] = enemy['position'] + (enemy['new_position'] - enemy['position']).normalize().elementwise()*.1

        if key['position'] == player['position'] and not key['collected']:
            key['collected'] = True
            game_map[5][2] = ft

        if chest['position'] == player['position']:
            nonlocal game_won
            game_won = True


    def draw_to_screen():
        DISPLAY_SURF.blit(background['sprite'], background['position'])

        temp_pos = pygame.Vector2(0, 0)
        for row in range(len(game_map)):
            for cel in range(len(game_map[0])):
                DISPLAY_SURF.blit(game_map[row][cel], temp_pos)
                # if game_map[row][cel] in collideable:
                #     DISPLAY_SURF.blit(debug_square, temp_pos)
                temp_pos = temp_pos + pygame.Vector2(TILE_DIMENSION, 0)
            temp_pos.x = 0
            temp_pos = temp_pos + pygame.Vector2(0, TILE_DIMENSION)
        for enemy in enemies:
            DISPLAY_SURF.blit(enemy['sprite'][animation_frame % len(enemy['sprite'])], enemy['position'].elementwise()*pygame.Vector2(TILE_DIMENSION))
        DISPLAY_SURF.blit(chest['sprite'], chest['position'].elementwise()*pygame.Vector2(TILE_DIMENSION))
        DISPLAY_SURF.blit(player['sprite'], player['position'].elementwise()*pygame.Vector2(TILE_DIMENSION))
        if not key['collected']:
            DISPLAY_SURF.blit(door['sprite'], door['position'].elementwise()*pygame.Vector2(TILE_DIMENSION))
            DISPLAY_SURF.blit(key['sprite'], key['position'].elementwise()*pygame.Vector2(TILE_DIMENSION))

        pygame.display.update()

    os.chdir(currentDir)

    while True:
        handle_input()
        update_world()
        draw_to_screen()

        if game_won:
            return True
        if game_lost:
            return False

        CLOCK.tick(60)

# dungeonGame()