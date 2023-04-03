import pygame as p
from random import randint

class Defender(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = p.image.load("SPACESHIP2.png")
        self.width = 150
        self.height = 150
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.life = 3

    def updatePosition(self, coordinates):
        self.rect.center = coordinates


class Missile(p.sprite.Sprite):
    def __init__(self, x, y, GameDisplay):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 10
        self.height = 20
        self.speed = 5
        self.image = p.Rect((self.x, self.y, self.width, self.height))
        self.rect = self.image
        self.missile_timer = 0
        self.color = (134, 255, 41)
        self.GameDisplay = GameDisplay


    def updatePosition(self, coordinates):
        self.rect.center = coordinates

    def printer(self):
        p.draw.rect(self.GameDisplay, self.color, self.rect)


class Enemy(p.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = p.image.load("SpaceEnemy.png")
        self.width = 75
        self.height = 75
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.life = 15
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.ticks = 0

    def randomMove(self):
        # direction = randint(1, 4)
        #
        # if direction == 1:
        #     self.rect.center = (self.rect.x, self.rect.y - 5)
        #
        # elif direction == 2:
        #     self.rect.center = (self.rect.x + 5, self.rect.y)
        #
        # elif direction == 3:
        #     self.rect.center = (self.rect.x - 5, self.rect.y)
        #
        # elif direction == 4:
        #     self.rect.center = (self.rect.x, self.rect.y + 5)
        self.rect.center = (self.rect.centerx + randint(-30, 30), self.rect.centery + randint(-30, 30))









class Rover(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.life = 0
        self.height = 100
        self.width = 100
        self.speed = 1
        self.image = p.image.load('Rover.png')
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.display_width = 650
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 650 - self.height



    def move(self):
        self.rect.x += self.speed
        if (self.rect.x > (self.display_width - self.width)) or (self.rect.x < 0):
            self.speed = -self.speed


