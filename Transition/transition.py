import pygame
import random
import os

def transition(programDir, text):
    SCREEN_SIZE = (1000, 1000)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    SCALED = 1000
    PASSON = False

    currentDir = os.getcwd()
    os.chdir(programDir)

    screens = [
        pygame.transform.scale(pygame.image.load('../assets/CurtainCall.png'), (SCALED, SCALED)),
        pygame.transform.scale(pygame.image.load('../assets/FinalFronteer.png'), (SCALED, SCALED))
    ]
    picked = random.choice(screens)

    os.chdir(currentDir)

    def handle_input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

    def draw_to_screen():
        nonlocal text
        nonlocal PASSON
        font = pygame.font.SysFont('Arial', 40)
        btext = font.render(text, True, (255, 255, 255))
        textrec = btext.get_rect(center=(1000 / 2, 1000 / 2))

        screen.blit(picked, (0, 0))
        screen.blit(btext, textrec)

        pygame.display.update()
        pygame.time.delay(2000)
        PASSON = True


    CLOCK = pygame.time.Clock()

    while True and not PASSON:
        handle_input()
        draw_to_screen()



        CLOCK.tick(60)

# transition(os.getcwd(), "Hello world")