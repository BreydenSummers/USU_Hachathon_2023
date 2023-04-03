import pygame
from pygame.locals import *
import random
import os

def pokeboss(programDir):
    pygame.init()

    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("BOSS FIGHT")
    TILE_SCALE = 200
    BGTILE_SCALE = 1000

    playerHealth = 100
    enemyHealth = 80
    playersTurn = True

    currentDir = os.getcwd()
    os.chdir(programDir)

    enemySprite = pygame.transform.scale(pygame.image.load("..\\Assets\\Sere.png").convert_alpha(), (TILE_SCALE, TILE_SCALE))
    playerSprite = pygame.transform.scale(pygame.image.load("..\\Assets\\Spook.png").convert_alpha(), (TILE_SCALE, TILE_SCALE))
    patchSprite = pygame.transform.scale(pygame.image.load("..\\Assets\\Patch.png").convert_alpha(), (TILE_SCALE, TILE_SCALE))
    bg = pygame.transform.scale(pygame.image.load("..\\Assets\\background.png").convert_alpha(), (BGTILE_SCALE, BGTILE_SCALE))
    heart = pygame.transform.scale(pygame.image.load("..\\Assets\\Heart.png").convert_alpha(), (TILE_SCALE, TILE_SCALE))
    attackOne = pygame.transform.scale(pygame.image.load("..\\Assets\\Move.png").convert_alpha(), (TILE_SCALE, TILE_SCALE))
    attackTwo = pygame.transform.scale(pygame.image.load("..\\Assets\\Move.png").convert_alpha(), (TILE_SCALE, TILE_SCALE))
    attackThree = pygame.transform.scale(pygame.image.load("..\\Assets\\Move.png").convert_alpha(), (TILE_SCALE, TILE_SCALE))
    attackFour = pygame.transform.scale(pygame.image.load("..\\Assets\\Move.png").convert_alpha(), (TILE_SCALE, TILE_SCALE))

    os.chdir(currentDir)

    class Button:
        def __init__(self, x, y, image, text):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False
            self.text = text
            self.font = pygame.font.SysFont('Arial', 25)

        def draw(self):
            action = False
            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Method to put individual buttons on the screen.
            btext = self.font.render(self.text, True, (255, 255, 255))
            textrec = btext.get_rect(center=(200 / 2, 160 / 2))
            recSurface = pygame.Surface(self.rect.size).convert()
            recSurface.blit(self.image, (0, -15))
            recSurface.blit(btext, textrec)
            screen.blit(recSurface, (self.rect.x, self.rect.y))
            return action

    # Buttons for my game
    attackOneButton = Button(80, 510, attackOne, "Basic : 21 DMG")
    attackTwoButton = Button(350, 510, attackTwo, "Pizza : +30HP")
    attackThreeButton = Button(80, 640, attackThree, "Sleep : no effect")
    attackFourButton = Button(350, 640, attackFour, "R.K.O. : 34 DMG")

    def handle_input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit


    recColor = (100 , 34, 39)
    enemyLastMove = ""
    def update_world():
        nonlocal playersTurn
        nonlocal playerHealth
        nonlocal enemyHealth
        nonlocal enemyLastMove
        if not playersTurn:
            enemiesAttack = random.randint(1,4)
            if enemyHealth > 0:
                if enemiesAttack == 1:
                    print("Enemy Attacks: WORK LIFE BALANCE")
                    enemyLastMove = "Enemy Attacks: WORK LIFE BALANCE: It dealt 20 damage"
                    playerHealth -= 40
                if enemiesAttack == 2:
                    print("Enemy Attacks: Yo mama!")
                    enemyLastMove = "Enemy Attacks: Yo mama! It dealt 10 damage"
                    playerHealth -= 10
                if enemiesAttack == 3:
                    print("Enemies Heals: Got Some Sleep. L")
                    enemyLastMove = "Enemies Heals: Got Some Sleep. It regained 10 HP"
                    enemyHealth += 40
                if enemiesAttack == 4:
                    print("Tried to Beat us in Hack USU: It doesn't effect us")
                    enemyLastMove = "Tried to Beat us in Hack USU: It doesn't effect us"
            playersTurn = True

    def draw_to_screen():
        nonlocal playersTurn
        nonlocal playerHealth
        nonlocal enemyHealth


        #Place holders for where the items will go
        screen.blit(bg, (0,0))
        screen.blit(patchSprite, (125, 160))

        screen.blit(patchSprite, (650, 350))
        pygame.draw.rect(screen, recColor, [0, 550, 1000, 300])
        if attackOneButton.draw() == True:
            enemyHealth -= 21
            playersTurn = False
            print("Rm -rf \\* (lol)")
        if attackTwoButton.draw() == True:
            playerHealth += 30
            playersTurn = False
            print("Thunderous Applause")
        if attackThreeButton.draw() == True:
            print("Sleep ---- Nah")
            playersTurn = False
        if attackFourButton.draw() == True:
            enemyHealth -= 34
            playersTurn = False
            print("Back Blast")

        screen.blit(enemySprite, (130, 100))
        screen.blit(playerSprite, (650, 300))

        font = pygame.font.SysFont('Arial', 16)
        btext = font.render(enemyLastMove, True, (255, 255, 255))
        textRect = btext.get_rect()
        textRect.center = (790, 700)
        screen.blit(btext, textRect)

        if playerHealth >= 81:
            screen.blit(heart, (((64* (0+1)) + 500), 500))
        if playerHealth >= 61:
            screen.blit(heart, (((64* (1+1)) + 500), 500))
        if playerHealth >= 41:
            screen.blit(heart, (((64* (2+1)) + 500), 500))
        if playerHealth >= 21:
            screen.blit(heart, (((64* (3+1)) + 500), 500))
        if playerHealth >= 1:
            screen.blit(heart, (((64* (4+1)) + 500), 500))
        if playerHealth <= 0:
            return False

        if enemyHealth >= 65:
            screen.blit(heart, (((64* (0+1)) - 50), -30))
        if enemyHealth >= 50:
            screen.blit(heart, (((64* (1+1)) - 50), -30))
        if enemyHealth >= 35:
            screen.blit(heart, (((64* (2+1)) - 50), -30))
        if enemyHealth >= 20:
            screen.blit(heart, (((64* (3+1)) - 50), -30))
        if enemyHealth >= 1:
            screen.blit(heart, (((64* (4+1)) - 50), -30))
        if enemyHealth <= 0:
            return True
        pygame.display.update()


    CLOCK = pygame.time.Clock()

    # def runBossFight():
    while True:
        handle_input()
        update_world()
        var = draw_to_screen()
        if var  != None:
            return var


        CLOCK.tick(60)

    # runBossFight()