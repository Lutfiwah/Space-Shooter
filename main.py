import pygame
import sys
import math
from random import randint
from pygame import mixer

pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Shooter Game")
icon = pygame.image.load("images/logo.jpg")
pygame.display.set_icon(icon)

# Load fonts
font = pygame.font.Font("font/GameOfSquids.ttf", 25)

# Initialize variables
bullet_state = "ready"

def showHiScore():  
    try:
        with open("highscore.txt", "r") as fileo:
            hiscore_value = fileo.readline().strip()
    except FileNotFoundError:
        hiscore_value = "0"
    
    hiscore = font.render("High-Score : " + str(hiscore_value), True, (255, 255, 255))
    screen.blit(hiscore, (500, 10))

def showScore(x, y, score_value):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((bulletY - enemyY), 2))
    return dist < 35

def player(x, y, playerImg):
    screen.blit(playerImg, (x, y))

def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))

def enemy(x, y, enemyImg):
    screen.blit(enemyImg, (x, y))

def main():
    global bullet_state

    # Load background music
    mixer.music.load("music/background.wav")
    mixer.music.play(-1)  # -1 for infinite playing of the song

    over = False
    score_value = 0
    try:
        with open("highscore.txt", "r") as fileo:
            hiscore_value = int(fileo.readline().strip())
    except FileNotFoundError:
        hiscore_value = 0

    # Load images
    backgroundImg = pygame.image.load("images/background.png")
    playerImg = pygame.image.load("images/player.png")
    global bulletImg
    bulletImg = pygame.image.load("images/bullet.png")
    blastImg = pygame.image.load("images/blast.png")

    # Player settings
    playerX = 370
    playerY = 500
    playerX_change = 0

    # Bullet settings
    bulletX = 0
    bulletY = 500
    bulletY_change = 10

    # Enemy settings
    enemyImg = [
        pygame.image.load("enemy/1.png"),
        pygame.image.load("enemy/1.png"),
        pygame.image.load("enemy/3.png"),
        pygame.image.load("enemy/4.png"),
        pygame.image.load("enemy/2.png"),
        pygame.image.load("enemy/3.png"),
        pygame.image.load("enemy/2.png"),
        pygame.image.load("enemy/4.png")
    ]
    enemyX = [randint(0, 720) for _ in range(8)]
    enemyY = [randint(10, 150) for _ in range(8)]
    enemyX_change = [2] * 8
    enemyY_change = [0] * 8

    while True:
        screen.blit(backgroundImg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -4
                if event.key == pygame.K_RIGHT:
                    playerX_change = 4
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound("music/laser.wav")
                        bullet_sound.play()
                        bulletX = playerX + 16  # Adjust bullet position to be centered on the player
                        bulletY = 500
                        bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    playerX_change = 0

        # Update player position
        playerX += playerX_change
        playerX = max(0, min(playerX, 743))

        # Update bullet position
        if bullet_state == "fire":
            bulletY -= bulletY_change
            bullet(bulletX, bulletY)

        # Bullet boundary check
        if bulletY <= 0:
            bulletY = 500
            bullet_state = "ready"

        # Update enemy position
        for i in range(len(enemyImg)):
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]

            # Collision detection
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 500
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = randint(0, 720)
                enemyY[i] = randint(10, 150)

            enemy(enemyX[i], enemyY[i], enemyImg[i])

        # Update player
        player(playerX, playerY, playerImg)

        # Display score
        showScore(10, 10, score_value)
        showHiScore()

        pygame.display.update()

        # High score update
        if score_value > hiscore_value:
            hiscore_value = score_value
            with open("highscore.txt", "w") as fileo:
                fileo.write(str(hiscore_value))

if __name__ == "__main__":
    main()
