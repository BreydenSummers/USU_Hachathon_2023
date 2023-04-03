import textwrap

import pygame
import os
from pygame.locals import *


def runCampfire(boxes, commands, programDir):
    pygame.init()

    SCREENWIDTH = 1000
    SCREENLENGTH = 1200

    screen = pygame.display.set_mode([SCREENWIDTH, SCREENLENGTH])

    position = 0
    leftRectangle = False
    rightRectangle = False
    centerRectangle = False
    font = pygame.font.SysFont('Arial', 25)
    fontbig = pygame.font.SysFont('Arial', 50)
    change_animation = pygame.event.custom_type()
    pygame.time.set_timer(change_animation, 400)
    SCALE_DIMENTSION = 1000
    animation_frame = 0

    currentDir = os.getcwd()
    os.chdir(programDir)

    frames = [
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-1.png'),
                                                       (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-2.png'),
                                                       (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-3.png'),
                                                       (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-4.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-5.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-6.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-7.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-8.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-9.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-10.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-11.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-12.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-13.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-14.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-15.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-16.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-17.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
        pygame.transform.scale(pygame.image.load('../assets/OuterNight/OuterAnim-18.png'),
                               (SCALE_DIMENTSION, SCALE_DIMENTSION)),
    ]
    filepng = [
        pygame.transform.scale(pygame.image.load('./assets/Fol.png'),
                               (225, 225)),
        pygame.transform.scale(pygame.image.load('./assets/F.png'),
                               (225, 225)),
    ]

    os.chdir(currentDir)

    obj =boxes[0]
    modeTwo = False
    modeThree = False
    cmd = commands [0]
    def moveLeft():
        temp = position - 1
        if temp < 0:
            return position
        else:
            return temp

    def moveRight():
        temp = position + 1
        if position >= len(boxes) - 1:
            return position
        else:
            return temp

    def handle_input():
        nonlocal position
        nonlocal obj
        nonlocal modeTwo
        nonlocal modeThree
        nonlocal cmd
        nonlocal boxes
        nonlocal commands

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                position = moveRight()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                position = moveLeft()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if modeTwo:
                    cmd = commands[position]
                    modeThree = True
                else:
                    obj = boxes[position]
                    if not obj.isdirectory:
                        commands.remove("cd")
                    if obj.name == "../":
                        commands = ["cd", "paste"]
                    
                    position = 0
                    boxes = commands
                    modeTwo = True

            if event.type == change_animation:
                nonlocal animation_frame
                # global animation_frame
                animation_frame = animation_frame + 1


    def update_world():
        nonlocal leftRectangle
        nonlocal rightRectangle
        nonlocal centerRectangle

        if position > 0:
            leftRectangle = True
        else:
            leftRectangle = False
        if position != len(boxes) - 1:
            rightRectangle = True
        else:
            rightRectangle = False
        if len(boxes) > 0:
            centerRectangle = True
        else:
            centerRectangle = False

    recColor = (81, 88, 99)
    RECT_HEIGHT = 100
    RECT_LENGTH = 200




    def drawLeftRectangle():
        nonlocal leftRectangle
        if leftRectangle:
            rect = pygame.draw.rect(screen, recColor, (75, 125, RECT_LENGTH, RECT_HEIGHT), 0)
            recSurface = pygame.Surface(rect.size).convert()
            if modeTwo:
                recSurface.blit(filepng[1], (-15, -55))
            else:
                if boxes[position - 1].isdirectory:
                    recSurface.blit(filepng[0], (-15, -55))
                else:
                    recSurface.blit(filepng[1], (-15, -55))
            if modeTwo:
                text = font.render(textwrap.shorten(boxes[position - 1], width=16), True, (255, 255, 255))
            else:
                text = font.render(textwrap.shorten(boxes[position - 1].name, width=16), True, (255, 255, 255))
            textrec = text.get_rect(center=(RECT_LENGTH/2, RECT_HEIGHT/2))
            recSurface.blit(text, textrec)
            screen.blit(recSurface, rect)

    def drawRightRectangle():
        nonlocal rightRectangle
        if rightRectangle:
            rect = pygame.draw.rect(screen, recColor, (675, 125, RECT_LENGTH, RECT_HEIGHT), 0)
            recSurface = pygame.Surface(rect.size).convert()
            if modeTwo:
                recSurface.blit(filepng[1], (-15, -55))
            else:
                if boxes[position + 1].isdirectory:
                    recSurface.blit(filepng[0], (-15, -55))
                else:
                    recSurface.blit(filepng[1], (-15, -55))
            if modeTwo:
                text = font.render(textwrap.shorten(boxes[position + 1], width=16), True, (255, 255, 255))
            else:
                text = font.render(textwrap.shorten(boxes[position + 1].name, width=16), True, (255, 255, 255))
            textrec = text.get_rect(center=(RECT_LENGTH / 2, RECT_HEIGHT / 2))
            recSurface.blit(text, textrec)
            screen.blit(recSurface, rect)


    def drawCenterRectangle():
        nonlocal centerRectangle
        if centerRectangle:
            rect = pygame.draw.rect(screen, recColor, (375, 125, RECT_LENGTH, RECT_HEIGHT), 0)
            recSurface = pygame.Surface(rect.size).convert()
            if modeTwo:
                recSurface.blit(filepng[1], (-15, -55))
            else:
                if boxes[position].isdirectory:
                    recSurface.blit(filepng[0], (-15, -55))
                else:
                    recSurface.blit(filepng[1], (-15, -55))
            if modeTwo:
                text = font.render(textwrap.shorten(boxes[position], width=16), True, (255, 255, 255))
            else:
                text = font.render(textwrap.shorten(boxes[position].name, width=16), True, (255, 255, 255))
            textrec = text.get_rect(center=(RECT_LENGTH / 2, RECT_HEIGHT / 2))
            recSurface.blit(text, textrec)
            screen.blit(recSurface, rect)

    def draw_to_screen():
        screen.fill((0, 0, 0))
        text = fontbig.render("Choose where to adventure next!", True, (255, 255, 255))
        text_rec = text.get_rect(center=(SCREENWIDTH/2, 50))
        screen.blit(text, text_rec)
        drawLeftRectangle()
        drawRightRectangle()
        drawCenterRectangle()
        screen.blit(frames[animation_frame % len(frames)], (0, 300))
        pygame.display.update()

    CLOCK = pygame.time.Clock()

    while True:
        handle_input()
        update_world()
        draw_to_screen()
        if modeThree:
            return obj, cmd
        CLOCK.tick(60)


# print(runCampfire())
