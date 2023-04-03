import pygame

pygame.init()

screen = pygame.display.set_mode([1000, 800])

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    screen = pygame.display.set_mode([1000, 800])
    test.runtest()

    pygame.display.flip()

pygame.quit()