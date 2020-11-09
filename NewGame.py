import pygame
from pygame import *

WIN_WIDTH = 1120 - 320
WIN_HEIGHT = 960 - 320
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 0
FLAGS = 0
CAMERA_SLACK = 30

def main():
    global level
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Climbers")
    timer = pygame.time.Clock()
    level = 0

    """player_img=pygame.image.load('startup.png')
    player_x= 370
    player_y=480
    player_x_change=0"""

    #bg = Surface((32,32))
    bg=pygame.image.load("mountainrange800.jpg")
    #bg.convert()
    #bg.fill(Color("#0094FF"))

    up = left = right = False
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    enemy = Enemy(32,32)
    platforms = []

    x = 0
    y = 0

    if level == 0:
        level = [
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                         E  ",
            "                            PPPPPPPPPPPPPPPP",
            "                            PPPPPPPPPPPPPPPP",
            "                            PPPPPPPPPPPPPPPP",
            "               PPPPP        PPPPPPPPPPPPPPPP",
            "                            PPPPPPPPPPPPPPPP",
            "                            PPPP           P",
            "                            PPPP           P",
            "                            PPPP     PPPPPPP",
            "                      PPPPPPPPPP     PPPPPPP",
            "                            PPPP     PPPPPPP",
            "       PPPP                 PPPP     PPPPPPP",
            "                            PPPP     PPPPPPP",
            "                            PPPP     PPPPPPP",
            "                            PPPP     PPPPPPP",
            "PPPPP                       PPPP     PPPPPPP",
            "PPP                         PPPP     PPPPPPP",
            "PPP                         PPPP     PPPPPPP",
            "PPP                         PPPP     PPPPPPP",
            "PPP         PPPPP           PPPP     PPPPPPP",
            "PPP                                     PPPP",
            "PPP                                     PPPP",
            "PPP                                     PPPP",
            "PPP                       PPPPPPPPPPPPPPPPPP",
            "PPP                       PPPPPPPPPPPPPPPPPP",
            "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
            "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
            "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
            "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
            "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",]

        #background = pygame.image.load("bg2.jpg")


    total_level_width = len(level[0]) * 32
    total_level_height = len(level) * 32

    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            x += 32
        y += 32
        x = 0

    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)
    entities.add(enemy)

    while 1:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit

            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False

        # draw background
        for y in range(20):
            for x in range(25):
                screen.blit(bg, (x * 32, y * 32))

        # draw background
        #screen.blit(background, camera.apply((0,0)))
        #draw entities
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        # update player, update camera, and refresh
        player.update(up, left, right, platforms)
        enemy.update(platforms)
        camera.update(player)
        pygame.display.flip()

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        try:
            return target.rect.move(self.state.topleft)
        except AttributeError:
            return map(sum, zip(target, self.state.topleft))

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l + HALF_WIDTH, -t +HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling left
    l = max(-(camera.width - WIN_WIDTH), l)   # stop scrolling right
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling bottom

    return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(200, 1200, 32, 32)


    def update(self, up, left, right, platforms):
        if self.rect.top > 1440 or self.rect.top < 0:
            main()
        if self.rect.left > 1408 or self.rect.right < 0:
            main()
        if up:
            if self.onGround:
                self.yvel = 0
                self.yvel -= 10 # only jump if on the ground
        if left:
            self.xvel = -10
        if right:
            self.xvel = 10
        if not self.onGround:
            self.yvel += 0.3 # only accelerate with gravity if in the air
            if self.yvel > 80: self.yvel = 80 # max falling speed
        if not(left or right):
            self.xvel = 0

        self.rect.left += self.xvel # increment in x direction
        self.collide(self.xvel, 0, platforms) # do x-axis collisions
        self.rect.top += self.yvel # increment in y direction
        self.onGround = False; # assuming we're in the air
        self.collide(0, self.yvel, platforms) # do y-axis collisions

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0: self.rect.right = p.rect.left
                if xvel < 0: self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                if yvel < 0:
                    self.rect.top = p.rect.bottom


class Enemy(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.yVel = 0
        self.xVel = 0
        self.image = Surface((32,32))
        self.image.fill(Color("#00FF00"))
        self.image.convert()
        self.rect = Rect(300, 1200, 32, 32)
        self.onGround = False
        self.right_dis = False

    def update(self, platforms):
        if not self.onGround:
            self.yVel += 0.3

        if self.rect.left == 96:
            self.right_dis = False
        if self.rect.right == 480:
            self.right_dis = True
        if not self.right_dis:
            self.xVel = 2
        if self.right_dis:
            self.xVel = -2

        self.rect.left += self.xVel # increment in x direction
        self.collide(self.xVel, 0, platforms) # do x-axis collisions
        self.rect.top += self.yVel # increment in y direction
        self.onGround = False; # assuming we're in the air
        self.collide(0, self.yVel, platforms) # do y-axis collisions

    def collide(self, xVel, yVel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xVel > 0: self.rect.right = p.rect.left
                if xVel < 0: self.rect.left = p.rect.right
                if yVel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                if yVel < 0:
                    self.rect.top = p.rect.bottom

class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        #self.image = Surface([32, 32], pygame.SRCALPHA, 32) #makes blocks invisible for much better artwork
        self.image = Surface((32,32)) #makes blocks visible for building levels
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("Alien2.png")




if __name__ == "__main__":
    main()
