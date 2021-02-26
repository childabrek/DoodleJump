import pygame
from pygame.locals import *
import sys
import random


class DoodleJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.green = pygame.image.load("assets/green.png").convert_alpha()
        pygame.font.init()
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 25)
        self.playerRight = pygame.image.load("assets/right.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("assets/right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load("assets/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("assets/left_1.png").convert_alpha()
        self.direction = 0
        self.playerx = 400
        self.playery = 400
        self.platforms = [[400, 500, 0, 0]]
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0

    def updatePlayer(self):
        if not self.jump:
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0

        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1
            self.direction = 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
        if not self.direction:
            self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
        else:
            self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))

    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10,
                                 self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        for p in self.platforms:
            print(self.platforms[1][1])
            print(self.cameray)
            check = self.platforms[1][1] - self.cameray
            if check > 600:
                platform = 0
                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                self.platforms.pop(0)
                self.score += 100

            self.screen.blit(self.green, (p[0], p[1] - self.cameray))

    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0, 700)
            platform = 0
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.screen.fill((255, 255, 255))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.playery - self.cameray > 700:
                self.cameray = 0
                self.score = 0
                # self.springs = []
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.playerx = 400
                self.playery = 400
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip()


DoodleJump().run()
