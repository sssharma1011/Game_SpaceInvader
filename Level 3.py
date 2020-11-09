import pygame
import random
import math
from pygame import mixer

pygame.init()# initial the pygame
# https://www.flaticon.com/

# create screen(width, hight)
screen=pygame.display.set_mode((800, 600))
#screen=pygame.display.set_mode((1366, 768))
#background image
bg=pygame.image.load("bg1.jpg")

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

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
enemy_img=[]
enemy_x= []
enemy_y=[]
enemy_x_change=[]
enemy_y_change=[]
num_of_enemies=6


#enemy
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('Alien1.png'))
    enemy_x.append( random.randint(0,735))
    enemy_y.append(random.randint(50,150))
    enemy_x_change.append(0.1)
    enemy_y_change.append(40)



#bullet
#READY: you cant see the bullet on the screen
#FIRE: Bullet is currently moving
#bullet image
bullet_img=pygame.image.load("bullet (1).png")
bullet_x= 0
bullet_y=480
bullet_x_change=0
bullet_y_change=1
bullet_state="ready"

#score
score_val=0
font =pygame.font.Font("freesansbold.ttf",32)
text_x=10
text_y=10

#Game Over
over_font =pygame.font.Font("freesansbold.ttf",64)

def game_over_text():
    over_text=over_font.render("GAME OVER", True,(255,255,255))
    screen.blit(over_text,(200, 250))

def show_score(x,y):
    score=font.render("Score: "+str(score_val), True,(255,255,255))
    screen.blit(score,(x, y))

def player(x,y):
    screen.blit(player_img,(x, y))

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bullet_img,(x+16, y+10))

def isCollision(enemy_x,enemy_y,bullet_x, bullet_y ):
    dis= math.sqrt(math.pow(enemy_x-bullet_x,2)+(math.pow(enemy_y-bullet_y, 2)))
    #dis=(((((enemy_x[i]-bullet_x)**2)-((enemy_y[i]-bullet_y)**2))**0.5)

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
                bullet_sound=mixer.Sound('laser.wav')
                bullet_sound.play()
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
            player_x_change= 0.1
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
    for i in range(num_of_enemies):
        #game over
        if enemy_y[i]>440:
            for j in range(num_of_enemies):
                enemy_y[i]=2000
            game_over_text()
            break

        enemy_x[i] +=enemy_x_change[i]
        # below if conditions was for creating boundaries for spaceship to be roam in so that it will show on the screen...
        if enemy_x[i]<=0:
            enemy_x_change[i]=0.1
            enemy_y[i]+=enemy_y_change[i]
        elif enemy_x[i]>= (800-64):
            enemy_x_change[i]= -0.1
            enemy_y[i]+=enemy_y_change[i]
        #collision
        collision=isCollision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if collision:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y=480
            bullet_state="ready"
            score_val+=10
            print(score_val)
            enemy_x[i]= random.randint(0,735)
            enemy_y[i]=random.randint(50,150)
        enemy(enemy_x[i], enemy_y[i], i)

    #bullet movement
    if bullet_y <=0:
        bullet_y=480
        bullet_state ="ready"
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)# bullet is not gonna appear if we remove it
        bullet_y -=bullet_y_change

    player(player_x, player_y)
    show_score(text_x,text_y)
    pygame.display.update()



pygame.quit()
