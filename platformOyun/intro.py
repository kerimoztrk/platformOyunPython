import pgzrun
import random 

from pgzhelper import *

WIDTH = 800
HEIGHT = 600

music.play('music')

black = (0, 0, 0)
brown = (71, 34, 18)
red = (212, 47, 47)
white = (255, 255, 255)

houses = Actor('houses')
houses.x = 500
houses.y = 400

bat = Actor('bat1')
bat.scale = 0.5
bat.x = 900
bat.y = 100
bat.images = ['bat1', 'bat2', 'bat3', 'bat4']
bat.fps = 10

zombie = Actor('walk1')
zombie.x = 100
zombie.y = 470
zombie.images = ['walk1', 'walk2', 'walk3', 'walk4', 'walk5', 'walk6', 'walk7', 'walk8', 'walk9', 'walk10']
zombie.fps = 60

ghost = Actor('ghost1')
ghost.x = random.randint(900, 5000)
ghost.y = random.randint(250, 350)

obstacles = []
obstaclesTime = 0

score = 0
gameOver = False
deathSound = False

velocity = 0
gravity = 1

def update():
    global velocity
    global score
    global obstaclesTime
    global gameOver, deathSound

    zombie.next_image()

    if keyboard.up and zombie.y == 470:
        velocity = -22
    zombie.y = zombie.y + velocity
    velocity = velocity + gravity

    if zombie.y > 470:
        velocity = 0
        zombie.y = 470

    bat.animate()
    bat.x -= 3
    if bat.x < -50:
        bat.x = random.randint(1000, 1500)
        bat.y = random.randint(100, 250)

    if gameOver == False:
        ghost.x -= 5
    if ghost.x < -50:
        ghost.x = random.randint(900, 5000)
        ghost.y = random.randint(250, 350)

    if zombie.colliderect(ghost):
        sounds.collect.play()
        ghost.x = random.randint(900, 5000)
        ghost.y = random.randint(250, 350)
        score += 5

    obstaclesTime += 1

    if obstaclesTime > random.randint(60, 7000):
        spike = Actor('spike')
        spike.x = 860
        spike.y = 500
        if gameOver == False:
            obstacles.append(spike)
            obstaclesTime = 0

    for spike in obstacles: 
        spike.x -= 8
        if spike.x < -50:
            obstacles.remove(spike)
            score += 1

    if zombie.collidelist(obstacles) != -1:
        gameOver = True
        obstacles.remove(spike)
        if deathSound == False:
            sounds.gameover.play()
        deathSound = True

def draw():
    screen.draw.filled_rect(Rect(0, 0, 800, 500), (black))
    if gameOver:
        screen.draw.text('Game Over', centerx=380, centery=150, color=(red))
        screen.draw.text('Score: ' + str(score), centerx=380, centery=50, color=(white))
        music.stop()
    else:
        houses.draw()
        bat.draw()
        ghost.draw()
        screen.draw.filled_rect(Rect(0, 500, 1200, 800), (brown))
        zombie.draw()
        screen.draw.text('Score: ' + str(score), (20, 20), color=(red), fontsize=30)
        for spike in obstacles:
            spike.draw()

pgzrun.go()
