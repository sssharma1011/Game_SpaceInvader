import pygame
import random
import math
pygame.init()# initial the pygame
# https://www.flaticon.com/

# create screen(width, hight)
screen=pygame.display.set_mode((800, 600))

#background image
bg=pygame.image.load("bg1.jpg")



#Title and Icom
pygame.display.set_caption("Space Invaders created by Shree")
app_icon=pygame.image.load("ufo.png")
pygame.display.set_icon(app_icon)

#player
player_img=pygame.image.load('startup.png')
player_x= 370
player_y=480
player_x_change=0


#enemy

enemy_img=pygame.image.load('Alien1.png')
enemy_x= random.randint(0,735)
enemy_y=random.randint(50,150)
enemy_x_change=0.1
enemy_y_change=40


#bullet
#READY: you cant see the bullet on the screen
#FIRE: Bullet is currently moving
#bullet image
bullet_img=pygame.image.load("bullet.png")
bullet_x= 0
bullet_y=480
bullet_x_change=0
bullet_y_change=1
bullet_state="ready"

score=0

def player(x,y):
    screen.blit(player_img,(x, y))

def enemy(x,y):
    screen.blit(enemy_img,(x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bullet_img,(x+16, y+10))

def isCollision(enemy_x,enemy_y,bullet_x, bullet_y ):
    dis= math.sqrt(math.pow(enemy_x-bullet_x,2)+(math.pow(enemy_y-bullet_y, 2)))
    #dis=(((((enemy_x-bullet_x)**2)-((enemy_y-bullet_y)**2))**0.5)

    if dis< 20:
        return True
    else:
        return False
#Game Loop
running=True
while running:
    #(we can google the RGB code)RGB- Red, Green, Blue    for dark of any  color use 255 for this color and for light color use 150 and make zero to other color

    screen.fill((0,0,0))
    #background image
    screen.blit(bg, (0,0))

    #player_x+=0.1
    #player_y+=0.01

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #if key stroke is pressed check whether its right or left
    if event.type==pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            if bullet_state is "ready":
                #get the current x coordinate of spaceship
                bullet_x=player_x
                fire_bullet(bullet_x,bullet_y)
                print("UP")
        if event.key==pygame.K_LEFT:
            player_x_change= -0.3
            print("Left arrow")
        if event.key==pygame.K_RIGHT:
            print("Right arrow")
            player_x_change= 0.3


    if event.type==pygame.KEYUP:
        if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
            player_x_change= 0.3
            print("Key Released")

    #5 = 5 + -0.1 -----> 5 = 5 - 0.1
    #5 = 5 + 0.1
    player_x +=player_x_change
    # below if conditions was for creating boundaries for spaceship to be roam in so that it will show on the screen...
    if player_x<=0:
        player_x=0
    elif player_x>= (800-64):
        player_x=(800-64)
    player(player_x, player_y)


    #enemy movement

    enemy_x +=enemy_x_change
    # below if conditions was for creating boundaries for spaceship to be roam in so that it will show on the screen...
    if enemy_x<=0:
        enemy_x_change=0.1
        enemy_y+=enemy_y_change
    elif enemy_x>= (800-64):
        enemy_x_change= -0.1
        enemy_y+=enemy_y_change


    #bullet movement
    if bullet_y <=0:
        bullet_y=480
        bullet_state ="ready"
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)# bullet is not gonna appear if we remove it
        bullet_y -=bullet_y_change
    #collision
    collision=isCollision(enemy_x,enemy_y,bullet_x,bullet_y)
    if collision:
        bullet_y=480
        bullet_state="ready"
        score+=10
        print(score)
        enemy_x= random.randint(0,735)
        enemy_y=random.randint(50,150)
    enemy(enemy_x, enemy_y)

    player(player_x, player_y)
    pygame.display.update()



