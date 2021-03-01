import pygame
from pygame.locals import *
import random
import sys


class DoodleJump:
    def __init__(self):
        # name program
        pygame.display.set_caption('PotatoJump')
        # size
        self.screen = pygame.display.set_mode((600, 800))
        # score_module
        pygame.font.init()
        self.score = 0
        self.font = pygame.font.SysFont(
            "sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold", 25)
        # loading picture
        self.green = pygame.image.load("assets/green.png").convert_alpha()
        self.blue = pygame.image.load("assets/blue.png").convert_alpha()
        self.red = pygame.image.load("assets/red.png").convert_alpha()
        self.red_1 = pygame.image.load("assets/red_1.png").convert_alpha()
        self.playerRight = pygame.image.load("assets/right.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("assets/right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load("assets/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("assets/left_1.png").convert_alpha()
        self.monster = pygame.image.load("assets/monsters.png").convert_alpha()
        print(self.monster.get_width(), self.monster.get_height())
        self.direction = 0
        # start pos
        self.player_x = 270
        self.player_y = 650
        self.platforms = [[250, 600, 0, 0], [250, 600, 0, 0]]
        # start variable
        self.monsters = []
        self.clock = pygame.time.Clock()
        self.cam_speed = 0
        self.jump = 0
        self.gravity = 0
        self.x_move = 0

    def gen_plat(self):
        for i in range(850, 0, -50):
            # choice platform
            chance = random.randint(0, 100)
            if chance < 40:
                platform = 0
            elif chance < 70:
                platform = 1
            else:
                platform = 2
            self.platforms.append([random.randint(0, 500), i, platform, 0])

    def update_player(self):
        if self.jump <= 0:
            # fall
            self.jump = 0
            self.player_y += self.gravity
            self.gravity += 0.3
        else:
            # fly
            self.player_y -= self.jump
            self.jump -= 0.3
        # control
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.x_move < 10:
                self.x_move += 0.6
            self.direction = 0
        elif key[K_LEFT]:
            if self.x_move > -10:
                self.x_move -= 0.6
            self.direction = 1
        else:
            if self.x_move > 0:
                self.x_move -= 1
            elif self.x_move < 0:
                self.x_move += 1
        # player transition to other side
        if self.player_x > 650:
            self.player_x = -50
        elif self.player_x < -50:
            self.player_x = 650
        self.player_x += self.x_move
        # camera moving
        if self.player_y - self.cam_speed <= 300:
            self.cam_speed -= 7
        # choice player picture
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.player_x, self.player_y - self.cam_speed))
            else:
                self.screen.blit(self.playerRight, (self.player_x, self.player_y - self.cam_speed))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.player_x, self.player_y - self.cam_speed))
            else:
                self.screen.blit(self.playerLeft, (self.player_x, self.player_y - self.cam_speed))

    def update_screen(self):
        for i in self.platforms:
            rect = pygame.Rect(i[0], i[1], self.green.get_width() - 10, 10)
            player = pygame.Rect(self.player_x, self.player_y - 40, self.playerRight.get_width() - 10,
                                 self.playerRight.get_height() + 20)
            if self.jump >= 0:
                if rect.colliderect(player) and self.gravity and self.player_y < (i[1] - self.cam_speed):
                    if i[2] != 2:
                        self.jump = 15
                        self.gravity = 0
                    else:
                        i[-1] = 1

            if i[2] == 1:
                if i[-1] == 1:
                    i[0] += 5
                    if i[0] > 550:
                        i[-1] = 0
                else:
                    i[0] -= 5
                    if i[0] <= 0:
                        i[-1] = 1

    def draw_plat(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cam_speed
            if check > 800:
                chance = random.randint(0, 100)
                if chance < 70:
                    platform = 0
                elif chance < 85:
                    platform = 1
                else:
                    platform = 2
                if self.score < 5000:
                    self.platforms.append([random.randint(0, 500), self.platforms[-1][1] - 50, platform, 0])
                elif self.score < 10000:
                    self.platforms.append([random.randint(0, 500), self.platforms[-1][1] - 60, platform, 0])
                else:
                    self.platforms.append([random.randint(0, 500), self.platforms[-1][1] - 80, platform, 0])
                self.platforms.pop(0)
                self.score = self.cam_speed * -1

                coords = self.platforms[-1]
                check = random.randint(0, 100)
                if check > 95 and platform == 0:
                    self.monsters.append([coords[0], coords[1] - 50, 0])

            if p[2] == 0:
                self.screen.blit(self.green, (p[0], p[1] - self.cam_speed))
            elif p[2] == 1:
                self.screen.blit(self.blue, (p[0], p[1] - self.cam_speed))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.red, (p[0], p[1] - self.cam_speed))
                else:
                    self.screen.blit(self.red_1, (p[0], p[1] - self.cam_speed))

            for i in self.monsters:
                self.screen.blit(self.monster, (i[0], i[1] - self.cam_speed))
                rect = pygame.Rect(i[0], i[1], self.monster.get_width() - 20, self.monster.get_height() - 10)
                player = pygame.Rect(self.player_x, self.player_y - 40, self.playerRight.get_width() - 10,
                                     self.playerRight.get_height() + 20)
                if player.colliderect(rect):
                    self.player_y = 10000

    def run(self):
        a = [0]
        self.gen_plat()
        while True:
            self.screen.fill((255, 255, 255))
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.player_y - self.cam_speed > 700:
                self.cam_speed = 0
                a.append(self.score)
                self.platforms = [[250, 600, 0, 0]]
                self.gen_plat()
                self.player_x = 270
                self.player_y = 610

            self.draw_plat()
            self.update_player()
            self.update_screen()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))

            self.screen.blit(self.font.render('HI:' + str(max(a)), -1, (0, 0, 0)), (25, 50))
            pygame.display.flip()


DoodleJump().run()
