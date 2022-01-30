""" TO DO
- Improve performance
- add fps debug counter
- add levels: for example a level after every 10 points, add changes to color of background when level change
- yknow maybe i should add obstacles to experiment
- idea: change size and/or speed when level changes, a two player mode: 
it would be more like a new game, not actually dying when hit yourself, animated head
- when finished: make into exe

"""
# Library Import
import pygame
from pygame.locals import *
from random import randint, uniform, choice
from math import sqrt
import sys, os
from pygame.transform import scale



# Pygame Setup
pygame.init()
FPS = 100
clock = pygame.time.Clock()
vec = pygame.math.Vector2
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

# Colors
WHITE = (255, 255, 255)
ORANGE = (255, 150, 0)
DARK_GRAY = (20, 20, 20)
GRAY = (40, 40, 40)
LIGHT_GRAY = (255,255,255)

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 620, 688
DISPLAY_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_SURF.fill(WHITE)
pygame.display.set_caption("Snake")
BACKGROUND_COLOR = DARK_GRAY
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(BACKGROUND_COLOR)

# Variables
score = 0
highscore = int(open(os.path.join(
    sourceFileDir,"highscore.txt"),'r') .read())
highscore_start = highscore
font = pygame.font.SysFont("bahnschrift", 35)
game_end = False

# Constants
SPEED = 3
BLOCK_LENGTH = 30
SNAKE_LENGTH = BLOCK_LENGTH -2
SNAKE_COLOR = WHITE
FOOD_COLOR = ORANGE
BLOCKS_ADDED_PER_FOOD = 2
GAME_BOX_WIDTH, GAME_BOX_HEIGHT = 600,600
GAME_BOX_X, GAME_BOX_Y= 10, 77

# Images

IMAGE_BANNER = pygame.image.load(os.path.join(
    sourceFileDir, os.path.join('assets', 'banner.png')))

# Sound
try:
    SOUND_C = pygame.mixer.Sound(os.path.join(
        sourceFileDir, os.path.join('assets', 'c.wav')))
    SOUND_E = pygame.mixer.Sound(os.path.join(
        sourceFileDir, os.path.join('assets', 'e.wav')))
    SOUND_G = pygame.mixer.Sound(os.path.join(
        sourceFileDir, os.path.join('assets', 'g.wav')))
    SOUND_B = pygame.mixer.Sound(os.path.join(
        sourceFileDir, os.path.join('assets', 'b.wav')))
    SOUND_CEG = pygame.mixer.Sound(os.path.join(
        sourceFileDir, os.path.join('assets', 'ceg.wav')))
except:
    pass

# Functions
def aligned(coords):
    if coords[0] % BLOCK_LENGTH == 0 and coords[1] % BLOCK_LENGTH == 0:
        return True
    else:
        return False
def random_color():
  return (randint(50,255),randint(50,255),randint(50,255))
def random_float(a, b):
    return round(uniform(a, b), 5)
def VX():
    l = []
    for i in range(50):
        b = randint(-30, 30)
        if abs(b) > 20:
            l.append(b)

    return choice(l)
# Objects
class Snake_Head():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = SPEED
        self.vx = 0
        self.vy = 0
        self.length = SNAKE_LENGTH
        self.color = SNAKE_COLOR

        self.surf = pygame.Surface((self.length, self.length))
        
        self.rect = self.surf.get_rect(topleft=(GAME_BOX_X + self.x+((BLOCK_LENGTH-SNAKE_LENGTH)/2), GAME_BOX_Y+ self.y+((BLOCK_LENGTH-SNAKE_LENGTH)/2)))

        self.loading = False
        self.pending_direction = None
        self.previous_aligned_point = (self.x, self.y)

    def update(self):
        global game_end

        pressed_keys = pygame.key.get_pressed()

        if self.loading == False:
            if pressed_keys[K_UP]:
                if self.vy != -self.speed and self.vy != self.speed:
                    self.loading = True
                    self.pending_direction = "up"
                    ## SOUND_C.play()
            if pressed_keys[K_LEFT]:
                if self.vx != -self.speed and self.vx != self.speed:
                    self.loading = True
                    self.pending_direction = "left"
                    ## SOUND_E.play()
            if pressed_keys[K_RIGHT]:
                if self.vx != -self.speed and self.vx != self.speed:
                    self.loading = True
                    self.pending_direction = "right"
                    ## SOUND_G.play()

            if pressed_keys[K_DOWN]:
                if self.vy != -self.speed and self.vy != self.speed:
                    self.loading = True
                    self.pending_direction = "down"
                    ## SOUND_B.play()

        if aligned((self.x, self.y)):
            self.previous_aligned_point = (self.x, self.y)
        if self.loading == True and aligned((self.x, self.y)):
            if self.pending_direction == "up":
                if self.vy != self.speed:
                    self.vx = 0
                    self.vy = -self.speed
                    self.loading = False
            if self.pending_direction == "left":
                if self.vx != self.speed:

                    self.vx = -self.speed
                    self.vy = 0
                    self.loading = False
            if self.pending_direction == "right":
                if self.vx != -self.speed:
                    self.vx = self.speed
                    self.vy = 0
                    self.loading = False

            if self.pending_direction == "down":
                if self.vy != -self.speed:
                    self.vx = 0
                    self.vy = self.speed
                    self.loading = False

        if self.x + self.length > GAME_BOX_WIDTH:
            game_end = True
        if self.x < 0:
            game_end = True
        if self.y + self.length > GAME_BOX_HEIGHT:
            game_end = True
        if self.y < 0:
            game_end = True

        self.previous_x = self.x
        self.previous_y = self.y

        self.x += self.vx
        self.y += self.vy

        self.rect.update(GAME_BOX_X + self.x+((BLOCK_LENGTH-SNAKE_LENGTH)/2), GAME_BOX_Y+ self.y+((BLOCK_LENGTH-SNAKE_LENGTH)/2), self.length, self.length)
        self.surf.fill(self.color)

class Snake_Body_Blocks():
    def __init__(self, object):
        self.x = object.previous_aligned_point[0]
        self.y = object.previous_aligned_point[1]
        self.length = SNAKE_LENGTH
        self.speed = SPEED
        self.color = LIGHT_GRAY

        self.surf = pygame.Surface((self.length, self.length))
        self.vx = 0
        self.vy = 0
        self.rect = self.surf.get_rect(topleft=(GAME_BOX_X + self.x+((BLOCK_LENGTH-SNAKE_LENGTH)/2), GAME_BOX_Y+ self.y+((BLOCK_LENGTH-SNAKE_LENGTH)/2)))
        self.direction = None
        self.previous_aligned_point = (self.x, self.y)

    def update(self, object):

        tx = object.previous_aligned_point[0]  # target x
        ty = object.previous_aligned_point[1]
        if tx > self.x:
            self.direction = "right"
            self.vx = self.speed
            self.vy = 0
        elif tx < self.x:
            self.direction = "left"
            self.vx = -self.speed
            self.vy = 0
        elif ty > self.y:
            self.direction = "down"
            self.vx = 0
            self.vy = self.speed
        elif ty < self.y:
            self.direction = "up"
            self.vx = 0
            self.vy = -self.speed

        if aligned((self.x, self.y)):
            self.previous_aligned_point = (self.x, self.y)
        self.previous_x = self.x
        self.previous_y = self.y

        self.x += self.vx
        self.y += self.vy

        self.rect.update(GAME_BOX_X + self.x+((BLOCK_LENGTH-SNAKE_LENGTH)/2), GAME_BOX_Y+ self.y+((BLOCK_LENGTH-SNAKE_LENGTH)/2), self.length, self.length)
        self.surf.fill(self.color)


class Food():
    def __init__(self):
        self.x = randint(0, GAME_BOX_WIDTH/BLOCK_LENGTH-1) * BLOCK_LENGTH
        self.y = randint(0, GAME_BOX_WIDTH/BLOCK_LENGTH-1) * BLOCK_LENGTH
        self.length = SNAKE_LENGTH
        self.color = FOOD_COLOR

        self.surf = pygame.Surface((self.length, self.length))
        self.rect = self.surf.get_rect(topleft=(GAME_BOX_X + self.x+((BLOCK_LENGTH-SNAKE_LENGTH)/2), GAME_BOX_Y+ self.y+((BLOCK_LENGTH-SNAKE_LENGTH)/2)))

    def update(self):

        self.rect.update(GAME_BOX_X + self.x+((BLOCK_LENGTH-SNAKE_LENGTH)/2), GAME_BOX_Y+ self.y+((BLOCK_LENGTH-SNAKE_LENGTH)/2), self.length, self.length)
        self.surf.fill(self.color)


class Checkered_Background():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.length = BLOCK_LENGTH
        self.surf_0 = pygame.Surface((self.length, self.length))
        self.rect_0 = self.surf_0.get_rect(topleft=(0,0))

    def update(self, x, y):

        self.rect_0.update(GAME_BOX_X + x, GAME_BOX_Y+ y, self.length, self.length)
        self.surf_0.fill(DARK_GRAY)

class Explosion_Particle():
    def __init__(self, x, y, v, radius, color):
        self.pos = vec(x, y)
        self.vel = vec(v, v)
        self.vel.x = random_float(-1, 1) * v
        self.vn = sqrt(v**2 - self.vel.x**2)
        self.vel.y = random_float(-1, 1) * self.vn
        self.radius = radius
        self.color = color

    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        pygame.draw.circle(DISPLAY_SURF, self.color,
                           (GAME_BOX_X +self.pos.x, GAME_BOX_Y+self.pos.y), self.radius)

# Object Variables
food = []
F0 = Food()
F1 = Food()
food.append(F0)
food.append(F1)

CB0 = Checkered_Background()
snake = []
snake.append(Snake_Head(x=round((GAME_BOX_WIDTH/BLOCK_LENGTH)/2)*BLOCK_LENGTH, y=round((GAME_BOX_WIDTH/BLOCK_LENGTH)/2)*BLOCK_LENGTH))
all_particles = []


# Game Loop
while True:
    
    
    # Event functions
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Background Display
    DISPLAY_SURF.blit(IMAGE_BANNER, (0, 0))
    
    x_offset = 1
    for x in range(0, int(GAME_BOX_WIDTH/BLOCK_LENGTH), 2):

        for y in range(0, int(GAME_BOX_WIDTH/BLOCK_LENGTH)):
            if y % 2 == 0:
                x_offset = 1
            else:
                x_offset = 0
            DISPLAY_SURF.blit(CB0.surf_0, CB0.rect_0)
            CB0.update((x+x_offset)*BLOCK_LENGTH, y*BLOCK_LENGTH)

    # Snake Self Collision Detection
    if len(snake) > 3:
        for snake_body in snake[3:]:

            if snake[0].rect.colliderect(snake_body):
                game_end = True
    
    # Snake Food Collision Detection
    for food_bit in food:
        if snake[0].rect.colliderect(food_bit):
            ##SOUND_CEG.play()
            score += 1
            if score > highscore:
                highscore += 1
            """
            for i in range(50):
                all_particles.append(Explosion_Particle(F0.x, F0.y, VX(
                                                ), 2, ORANGE))
            """
            while True:
                food_pos_is_good = True
                pending_food_x = randint(0, GAME_BOX_WIDTH/BLOCK_LENGTH-1) * BLOCK_LENGTH
                pending_food_y = randint(0, GAME_BOX_WIDTH/BLOCK_LENGTH-1) * BLOCK_LENGTH
                temp_surf = pygame.Surface((BLOCK_LENGTH, BLOCK_LENGTH))
                temp_rect = temp_surf.get_rect(
                    topleft=(GAME_BOX_X + pending_food_x, GAME_BOX_Y +pending_food_y))
                for i in snake:
                    if i.rect.colliderect(temp_rect):
                        food_pos_is_good = False
                        break

                if food_pos_is_good:
                    food_bit.x = pending_food_x
                    food_bit.y = pending_food_y
                    for i in range(BLOCKS_ADDED_PER_FOOD):
                        snake.append(Snake_Body_Blocks(snake[-1]))
                    snake[-1].color = WHITE
                    
                    break
        

    # Snake Head Display
    DISPLAY_SURF.blit(snake[0].surf, snake[0].rect)
    snake[0].update()
    # Snake Body Display
    if snake[1:] != None:
        for i in snake[1:]:
            DISPLAY_SURF.blit(i.surf, i.rect)
            i.update(snake[snake.index(i)-1])

    # Font Display
    text_0 = font.render(str(score), True, WHITE)
    text_rect_0 = text_0.get_rect(topleft=(275, 25))
    DISPLAY_SURF.blit(text_0, text_rect_0)

    text_1 = font.render(str(highscore), True, WHITE)
    text_rect_1 = text_1.get_rect(topleft=(405, 25))
    DISPLAY_SURF.blit(text_1, text_rect_1)

    # Food Display
    for i in food:
        DISPLAY_SURF.blit(i.surf,i.rect)
        i.update()

    # Particles
    for entity in all_particles:
        entity.update()
    
    # Game End
    if game_end == True:
        pressed_keys = pygame.key.get_pressed()
        temp_surf_2 = pygame.Surface((400,60))
        temp_surf_2.fill(DARK_GRAY)
        temp_rect_2 = temp_surf_2.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+3))
        DISPLAY_SURF.blit(temp_surf_2, temp_rect_2)
        text_0 = font.render("Press Space to Retry", True, ORANGE)
        text_rect_0 = text_0.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        DISPLAY_SURF.blit(text_0, text_rect_0)
        
        for i in snake:
            i.x -= i.vx *2
            i.y -= i.vy * 2
            i.vx = 0
            i.vy = 0
            i.speed = 0

        
        if pressed_keys[K_SPACE]:

            if int(highscore_start) < highscore:
                with open(os.path.join(
                    sourceFileDir,"highscore.txt"), 'w') as file: 
                    file.write(str(highscore))

            score = 0
        
            food = []
            F0 = Food()
            F1 = Food()
            food.append(F0)
            food.append(F1)
            CB0 = Checkered_Background()
            snake = []
            game_end = False
            snake.append(Snake_Head(x=round((GAME_BOX_WIDTH/BLOCK_LENGTH)/2)*BLOCK_LENGTH, y=round((GAME_BOX_WIDTH/BLOCK_LENGTH)/2)*BLOCK_LENGTH))
            all_particles = []

    # Update Stuff
    pygame.display.update()
    clock.tick(FPS)
    print(clock.get_fps())




