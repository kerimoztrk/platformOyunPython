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

class GameObject(Actor):
    def __init__(self, image, x, y, **kwargs):
        super().__init__(image)
        self.x = x
        self.y = y
        self.__dict__.update(kwargs)

class AnimatedObject(GameObject):
    def __init__(self, image, x, y, images, fps, **kwargs):
        super().__init__(image, x, y, **kwargs)
        self.images = images
        self.fps = fps


houses = GameObject('houses', 500, 400)

bat = AnimatedObject('bat1', 900, 100, ['bat1', 'bat2', 'bat3', 'bat4'], 10, scale=0.5)

zombie = AnimatedObject('walk1', 100, 470, [
    'walk1', 'walk2', 'walk3', 'walk4', 'walk5', 
    'walk6', 'walk7', 'walk8', 'walk9', 'walk10'
], 60)

ghost = GameObject('ghost1', random.randint(900, 5000), random.randint(250, 350))

platforms = [GameObject('platform', 200, 400), GameObject('platform', 400, 300)]

obstacles = []
obstaclesTime = 0

score = 0
gameOver = False
deathSound = False
velocity = 0
gravity = 1


gameState = "menu"  
menuButtons = [
    {"text": "Oyna", "rect": Rect(300, 250, 200, 50), "action": "play"},
    {"text": "Müzik Aç/Kapa", "rect": Rect(300, 320, 200, 50), "action": "toggle_music"},
    {"text": "Çıkış", "rect": Rect(300, 390, 200, 50), "action": "exit"}
]
musicOn = True

def update():
    global velocity, score, obstaclesTime, gameOver, deathSound, gameState, musicOn

    if gameState == "play":
        zombie.next_image()

        if keyboard.up and is_on_ground():
            velocity = -22 
        zombie.y += velocity
        velocity += gravity

        if is_on_ground():
            velocity = 0

        bat.animate()
        bat.x -= 3
        if bat.x < -50:
            bat.x = random.randint(1000, 1500)
            bat.y = random.randint(100, 250)

        if not gameOver:
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

        if obstaclesTime > random.randint(100, 1200):  
            spike = GameObject('spike', 860, 500)
            if not gameOver:
                obstacles.append(spike)
                obstaclesTime = 0

        for spike in obstacles:
            spike.x -= 8
            if spike.x < -50:
                obstacles.remove(spike)
                score += 1

        if zombie.collidelist(obstacles) != -1:
            gameOver = True
            gameState = "gameover"
            if not deathSound:
                sounds.gameover.play()
            deathSound = True

        
        for platform in platforms:
            platform.x -= 3 
            if platform.x < -100:
                platform.x = WIDTH + 100
                platform.y = random.randint(250, 400)  

def draw():
    global gameState

    screen.clear()

    if gameState == "menu":
        screen.draw.text("Ana Menü", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color=white)
        for button in menuButtons:
            screen.draw.filled_rect(button["rect"], red)
            screen.draw.text(button["text"], center=button["rect"].center, fontsize=30, color=white)

    elif gameState == "play":
        screen.draw.filled_rect(Rect(0, 0, 800, 500), (black))
        houses.draw()
        bat.draw()
        ghost.draw()
        screen.draw.filled_rect(Rect(0, 500, 1200, 800), (brown))
        zombie.draw()
        for platform in platforms:
            platform.draw()
        screen.draw.text('Score: ' + str(score), (20, 20), color=(red), fontsize=30)
        for spike in obstacles:
            spike.draw()

    elif gameState == "gameover":
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 3), fontsize=50, color=red)
        screen.draw.text("Skor: " + str(score), center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color=white)
        screen.draw.text("Ana Menü için Enter'a basın", center=(WIDTH // 2, HEIGHT // 1.5), fontsize=30, color=white)

def is_on_ground():
    if zombie.y >= 470:
        return True
    for platform in platforms:
        if zombie.colliderect(platform) and zombie.y < platform.y:
            return True
    return False

def on_mouse_down(pos):
    global gameState, musicOn

    if gameState == "menu":
        for button in menuButtons:
            if button["rect"].collidepoint(pos):
                action = button["action"]
                if action == "play":
                    reset_game()
                    gameState = "play"
                elif action == "toggle_music":
                    musicOn = not musicOn
                    if musicOn:
                        music.play('music')
                    else:
                        music.stop()
                elif action == "exit":
                    exit()

def on_key_down(key):
    global gameState

    if gameState == "gameover" and key == keys.RETURN:
        gameState = "menu"

def reset_game():
    global obstacles, obstaclesTime, score, gameOver, deathSound, velocity
    obstacles = []
    obstaclesTime = 0
    score = 0
    gameOver = False
    deathSound = False
    velocity = 0

pgzrun.go()
