import time
import os
import pygame as p
from random import randint

def ck(programDir):
    currentDir = os.getcwd()
    os.chdir(programDir + "\\" + "CosmicKiller\\")
    print(os.getcwd())
    p.init()

    from CosmicKiller.characters import Defender, Missile, Rover, Enemy

    winner = False

    display_width = 800
    display_height = 650

    background_image = p.image.load('Space.png')
    background_image = p.transform.scale(background_image, (display_width, display_height))

    p.mouse.set_visible(False)

    gameDisplay = p.display.set_mode((display_width, display_height))
    p.display.set_caption("👽-COSMIC KILLER-👽")

    clock = p.time.Clock()

    # define group for all sprites
    all_sprites = p.sprite.Group()

    # defender properties
    defender = Defender()
    all_sprites.add(defender)

    # missile properties
    missile_speed = 5
    missile_height = 20
    missile_width = 10
    missiles = []

    # rover properties
    rover = Rover()
    all_sprites.add(rover)

    enemies = []

    the_time = time.time()
    ticker = 0




    def startEnemies(number_enemies):
        for i in range(number_enemies):
            enemies.append(Enemy(randint(50, 750), randint(50, 400)))

        for enemy in enemies:
            all_sprites.add(enemy)


    # create the enemies
    startEnemies(5)


    def shoot_missile(ship_x, ship_y):
        missile = Missile(ship_x, ship_y, gameDisplay)
        missiles.append(missile)


    def loop():

        gameExit = False
        missile_timer = 0

        while not gameExit:
            # shoot the missile if the button is pressed. shoots continuously
            leftshooter_x = p.mouse.get_pos()[0] - 45
            leftshooter_y = p.mouse.get_pos()[1] - 35

            rightshooter_x = p.mouse.get_pos()[0] + 32
            rightshooter_y = p.mouse.get_pos()[1] - 35
            if p.mouse.get_pressed()[0] and (p.time.get_ticks() - missile_timer > 200):
                shoot_missile(leftshooter_x, leftshooter_y)
                shoot_missile(rightshooter_x, rightshooter_y)
                missile_timer = p.time.get_ticks()

            nonlocal ticker
            if ticker > 25:
                ticker = 0
                for enemy in enemies:
                    enemy.randomMove()
            else:
                ticker += 1

            for missile in missiles:
                missile.image.move_ip(0, -missile_speed)
                if missile.rect.centery <= 0:
                    print(missile.rect.center)
                    missile.rect = p.Rect(0, 0, 0, 0)
                    missiles.remove(missile)
                    missile.kill()


            for event in p.event.get():
                if event.type == p.QUIT:
                    gameExit = True
                    p.quit()
                    quit()
                if event.type == p.KEYDOWN and event.key == p.K_BACKSPACE:
                    gameExit = True

            gameDisplay.blit(background_image, (0, 0))
            defender.updatePosition(p.mouse.get_pos())

            rover.move()
            all_sprites.draw(gameDisplay)

            for missile in missiles:
                missile.printer()
                for enemy in enemies:
                    if p.sprite.collide_rect(missile, enemy):
                        enemy.life -= 1
                        missile.rect = p.Rect(0, 0, 0, 0)
                        if enemy.life <= 0:
                            enemies.remove(enemy)
                            enemy.rect = p.Rect(0, 0, 0, 0)
                            enemy.kill()
                            print(enemies)
            p.display.update()
            if len(enemies) == 0:
                return True
    os.chdir(currentDir)
    return loop()


    # starship()
    # loop()
    # p.quit()
    # quit()
