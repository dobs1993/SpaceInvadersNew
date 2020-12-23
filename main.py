import pygame
import random
import math
from pygame import mixer



#initilize
pygame.init()

#create screen
screen = pygame.display.set_mode((800, 600))

#background

background = pygame.image.load('background1.png')

#background sound

mixer.music.load('background.wav')
mixer.music.play(-1)

#title and icon

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)


#player on screen
player_img = pygame.image.load('space-invaders.png')
player_x = 370
player_y = 480
player_x_change = 0

#enemy on screen
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(10)
    enemy_y_change.append(43)

#bullet on screen

#ready state means you cant see the bullet on the screen
#fire means the bullet is moving
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

#game over

game_finish_text = pygame.font.Font('freesansbold.ttf', 64)

#score

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

text_x = 10
text_y = 10

def show_score(x, y):
    score = font.render("score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    game_text = game_finish_text.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_text, (200, 250))

def player(x,y):
    screen.blit(player_img, (x, y))

def enemy(x,y,i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x-bullet_x, 2)) + (math.pow(enemy_y-bullet_y, 2)))
    if distance < 27:
        return True
    return False

#game loop - main component of game


running = True
while running:

    # changing the background color while in the while loop which means the game is running
    screen.fill((100, 10, 10))
    #background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #if key stroke is pressed check whether is right or left

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change -= 5
            elif event.key == pygame.K_RIGHT:
                player_x_change += 5
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, player_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0


#checking boundaies for space ship so it doesnt go out of bounds
    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

#enemy controller
    for i in range(num_of_enemies):

        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2200
            game_over_text()
            break


        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 10
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -10
            enemy_y[i] += enemy_y_change[i]

        # collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        # enemy
        enemy(enemy_x[i], enemy_y[i], i)

    #bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change


    player(player_x, player_y)

    #pygame.display.get_active()

    show_score(text_x, text_y)

#update everything within pygame
    pygame.display.update()

