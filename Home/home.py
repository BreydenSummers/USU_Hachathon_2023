import pygame
import random
import os

def homeGame(programDir):
    # constants
    TILE_DIMENSION = 140
    SCREEN_SIZE = (13*70, 11*70)
    ORIGIN_POSITION = pygame.Vector2(2, 4)

    sky_blue = pygame.Surface((TILE_DIMENSION, TILE_DIMENSION))
    sky_blue.fill((180, 200, 255))

    currentDir = os.getcwd()
    os.chdir(programDir)

    # assets
    sb = pygame.transform.scale(pygame.image.load('../assets/Cloud.png'), (TILE_DIMENSION,TILE_DIMENSION))
    bl = pygame.transform.scale(pygame.image.load('../assets/Plainhome_3.png'), (TILE_DIMENSION, TILE_DIMENSION))
    tl = pygame.transform.flip(bl, 0, 1)
    br = pygame.transform.flip(bl, 1, 0)
    tr = pygame.transform.flip(br, 0, 1)
    re = pygame.transform.scale(pygame.image.load('../assets/Plainhome_4.png'), (TILE_DIMENSION, TILE_DIMENSION))
    le = pygame.transform.flip(re, 1, 0)
    te = pygame.transform.scale(pygame.image.load('../assets/Plainhome_2.png'), (TILE_DIMENSION, TILE_DIMENSION))
    be = pygame.transform.flip(te, 0, 1)
    ft = pygame.transform.scale(pygame.image.load('../assets/Plainhome_5.png'), (TILE_DIMENSION, TILE_DIMENSION))
    ot = pygame.transform.scale(pygame.image.load('../assets/Plainhome_5.png'), (TILE_DIMENSION, TILE_DIMENSION))


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
        [sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, ],
        [sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, ],
        [sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, ],
        [sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, ],
        [sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, sb, ],
        [ft, ft, ft, bl, be, be, be, be, be, be, be, be, be, be, be, br, ft, ft, ft, ],
        [te, te, te, tl, te, te, te, te, te, te, te, te, te, te, te, re, te, te, te, ],
        [ft, ft, ft, le, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, re, ft, ft, ft, ],
        [ft, ft, ft, le, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, re, ft, ft, ft, ],
        [ft, ft, ft, le, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, ft, re, ft, ft, ft, ],
        [ft, ft, ft, bl, be, be, be, be, be, be, be, be, be, be, be, br, ft, ft, ft, ],
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
    player = {
        'sprite': pygame.transform.scale(pygame.image.load("../assets/HumanAsset.png"), (TILE_DIMENSION, TILE_DIMENSION)),
        'position': pygame.Vector2(8, 9),
        'new_position': pygame.Vector2(8, 9),
        'moving_left': False,
    }

    pedestals = []
    files = []
    pedestals_positions = [
        pygame.Vector2(10, 7),
        pygame.Vector2(8, 7),
        pygame.Vector2(6, 7),
        pygame.Vector2(12, 7),
        pygame.Vector2(14, 7),
    ]
    file_positions = [
        pygame.Vector2(10, 6),
        pygame.Vector2(8, 6),
        pygame.Vector2(6, 6),
        pygame.Vector2(12, 6),
        pygame.Vector2(14, 6),
    ]
    for i in range(len(file_positions)):
        files.append(
            {
                #'sprite': sb.copy(),
                'sprite': pygame.transform.scale(pygame.image.load('../assets/File.png'),(TILE_DIMENSION, TILE_DIMENSION)),
                'position': file_positions[i],
                'new_position': file_positions[i],
                'visible': False,
            }
        )
    for enemy in files:
        enemy['sprite'].set_alpha(0)

    for i in range(len(pedestals_positions)):
        pedestals.append(
            {
                'sprite': pygame.transform.scale(pygame.image.load('../assets/Pedestal_.png'),(TILE_DIMENSION, TILE_DIMENSION)),
                'position': pedestals_positions[i],
                'new_position': pedestals_positions[i],
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

    vase = {
        'sprite': pygame.transform.scale(pygame.image.load('../assets/Vase.png'), (TILE_DIMENSION, TILE_DIMENSION)),
        'position': pygame.Vector2(7, 7),
    }

    background = {
        'sprite': pygame.image.load("../assets/background.png"),
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
            return new_position

    movedUp = False

    def handle_input():
        nonlocal movedUp
        nonlocal game_won

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if not movedUp:
                    print("I moved up")
                    movedUp = True
                    player['new_position'] = calculate_new_position((0, -1), player)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if movedUp:
                    game_won = True



        # if not inputDisabled:
        #     keys_pressed = pygame.key.get_pressed()
        #     if keys_pressed[pygame.K_RIGHT]:
        #         player['new_position'] = calculate_new_position((1, 0), player)
        #         if player['moving_left']:
        #             player['sprite'] = pygame.transform.flip(player['sprite'], 1, 0)
        #             player['moving_left'] = False
        #     if keys_pressed[pygame.K_LEFT]:
        #         player['new_position'] = calculate_new_position((-1, 0), player)
        #         if not player['moving_left']:
        #             player['sprite'] = pygame.transform.flip(player['sprite'], 1, 0)
        #             player['moving_left'] = True
        #     if keys_pressed[pygame.K_DOWN]:
        #         player['new_position'] = calculate_new_position((0, 1), player)
        #     if keys_pressed[pygame.K_UP]:
        #         player['new_position'] = calculate_new_position((0, -1), player)


    def update_world():
        nonlocal inputDisabled
        if player['position'] != player['new_position']:
            inputDisabled = True
            player['position'] = player['position'] + (player['new_position'] - player['position']).normalize().elementwise()*.1
        else:
            inputDisabled = False

        for enemy in files:
            if player['position'] == (enemy['position']+pygame.Vector2(0, 2)):
                enemy['visible'] = True
            else:
                enemy['visible'] = False
            if enemy['visible']:
                temp_a = enemy['sprite'].get_alpha()
                enemy['sprite'].set_alpha(temp_a+5 if temp_a < 255 else temp_a)
            else:
                enemy['sprite'].set_alpha(0)





        if key['position'] == player['position'] and not key['collected']:
            key['collected'] = True
            game_map[5][2] = ft

        if chest['position'] == player['position']:
            nonlocal game_won
            game_won = True


    def draw_to_screen():
        nonlocal movedUp
        DISPLAY_SURF.blit(background['sprite'], background['position'])

        temp_pos = pygame.Vector2(0, 0)
        for row in range(len(game_map)):
            for cel in range(len(game_map[0])):
                DISPLAY_SURF.blit(game_map[row][cel], (temp_pos-(player['position'].elementwise()-ORIGIN_POSITION)).elementwise()*pygame.Vector2(TILE_DIMENSION))
                # if game_map[row][cel] in collideable:
                #     DISPLAY_SURF.blit(debug_square, temp_pos)
                temp_pos = temp_pos + pygame.Vector2(1, 0)
            temp_pos.x = 0
            temp_pos = temp_pos + pygame.Vector2(0, 1)
        for enemy in pedestals:
            DISPLAY_SURF.blit(enemy['sprite'], (enemy['position']-(player['position'].elementwise()-ORIGIN_POSITION)).elementwise()*pygame.Vector2(TILE_DIMENSION))
        for enemy in files:
            DISPLAY_SURF.blit(enemy['sprite'], (enemy['position']-(player['position'].elementwise()-ORIGIN_POSITION)).elementwise()*pygame.Vector2(TILE_DIMENSION))
        DISPLAY_SURF.blit(chest['sprite'], (chest['position']-(player['position'].elementwise()-ORIGIN_POSITION)).elementwise()*pygame.Vector2(TILE_DIMENSION))
        DISPLAY_SURF.blit(player['sprite'], ORIGIN_POSITION.elementwise()*pygame.Vector2(TILE_DIMENSION))
        DISPLAY_SURF.blit(vase['sprite'], (vase['position']-(player['position'].elementwise()-ORIGIN_POSITION)).elementwise()*pygame.Vector2(TILE_DIMENSION))
        if movedUp:
            font = pygame.font.Font('freesansbold.ttf', 26)
            text = font.render("Do you wish to participate in a file exploration?", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (400, 200)
            DISPLAY_SURF.blit(text, textRect)
            text = font.render("If so press enter.", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (400, 226)
            DISPLAY_SURF.blit(text, textRect)
        else:
            font = pygame.font.Font('freesansbold.ttf', 26)
            text = font.render("Press the up arrow key to move", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (400, 200)
            DISPLAY_SURF.blit(text, textRect)

        pygame.display.update()

    os.chdir(currentDir)

    while True:
        handle_input()
        update_world()
        draw_to_screen()

        if game_won:
            return True

        CLOCK.tick(60)

# homeGame()
