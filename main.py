import pygame
from Dungeon.main import dungeonGame
from Home.home import homeGame
from Fileexplorer.main import Files, Child, ClipBoard
from campfire.main import runCampfire
from Transition.transition import transition
from BossFight.bossscript import pokeboss
from CosmicKiller.main import ck
import os
import random

programDir = os.getcwd()

pygame.init()

games = [dungeonGame, pokeboss, ck] #, homeGame]

screen = pygame.display.set_mode([1000, 800])
f = Files(True)
f.children.append(Child(True, "../", True))
running = True
clippy = ClipBoard(None, None)
homeGame(programDir)
gamechoice = 0
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen = pygame.display.set_mode([13*70, 11*70])



    cmd = ["cd", "run", "copy", "paste"]
    result = runCampfire(f.children, cmd, programDir)
    gamechoice = gamechoice + 1
    win = games[gamechoice % 3](programDir)
    if win:
        try:
            if result[1] == "cd":
                if result[0].permission:
                    f = f.cd(result[0].name)
                    f.children.append(Child(True, "../", True))

            elif result[1] == "run":
                if result[0].permission:
                    f.lf(result[0].name)
            elif result[1] == "copy":
                if result[0].permission:
                    clippy = f.copy(result[0].name)
            elif result[1] == "paste":
                if result[0].permission:
                    f.paste(clippy)
        except OSError:
            print("Permission error!")
        transition(programDir, "The Explorer survives harrowing experience...")
    else:
        transition(programDir, "The Explorer crawled their way back to camp...")
        print("You lost")

    pygame.display.flip()

pygame.quit()