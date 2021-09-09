import pygame
import random
import time
import os
from pygame import mixer
from pygame import freetype


os.chdir(r"G:\coding\PythonProjects\PALLAV PROJECTS\python games\mouse game")
pygame.init()
mixer.init()
mixer.music.load("BGtheme.mp3")
hit_sound = mixer.Sound("dmg_sound.mp3")

mixer.music.set_volume(0.1)
mixer.music.play(-1)

gamefont = freetype.SysFont("comicsansms", 20)

kill_zone = []                                    # LIST CONTAINING COORDINATES OF BOXES
game_area_ulim = 60                               # START DISPLAYING BOXES BELOW THESE PIXEL 
speed = 0.6                                       # X SPEED AT WHICH BOXES SCROLL
gap = 100                                         # VERTICAL ENTRANCE GAP BETWEEN UP AND DOWN BOXES
seperation = 150                                  # SPACE BETWEEN CONSECUTIVE BOXES (LEFT-RIGHT) 
tx = 0                                            # DISTANCE MOVED IN -X DIRECTION
width = 50                                        # THICKNESS OF BLOCKS
deviation = 100                                   # RANGE OF RANDOM PLACEMENT OF GAP ABOVE MID
invincible_time = 0                               # TEMP VARIABLE, DO NOT CHANGE
grant_shield_time = 1                             # INVINCIBILITY TIME GRANTED AFTER EACH HIT
score = 0
life = 5
box_colour = [255,0,0]
disp = 400                                        # POSITION TO START STARTING BARS
ini_bars = 8                                      # BARS TO PUT PRERENDERED INTO LIST
run = True                                        # STOP RUNNING (EXIT) IF SET TO FALSE



window = pygame.display.set_mode((960, 540+game_area_ulim))
pygame.display.set_caption('Pallav Game')

pygame.draw.line(window, box_colour, (0, game_area_ulim-1), (960, game_area_ulim-1), 1)
text_surface, rect = gamefont.render(f"LIVES = {life}", (0, 200, 200))
window.blit(text_surface, (20, 20))


# INITIAL VALUE PROVIDER
for i in range(ini_bars):
    ulim = random.randint(270-deviation, 270+deviation)
    kill_zone.append([seperation*i + disp, game_area_ulim, width, ulim])
    kill_zone.append([seperation*i + disp, game_area_ulim + ulim+gap, width, 540-ulim-gap])

# CHECK IF MOUSE IS IN BOX
def check_if_in(mouse_x, mouse_y):
    for box in kill_zone:
        if mouse_x > box[0] and mouse_x < box[0]+box[2]:
            if mouse_y > box[1] and mouse_y <box[1] + box[3]:
                return True
    return False

# CHECK IF PLAYER IS NOT IN SAFE MODE AND DEAL DAMAGE
def deal_dmg():
    global life
    global invincible_time
    global text_surface
    global rect
    
    if time.time() > invincible_time:
        life -= 1
        hit_sound.play()
        invincible_time = time.time() + grant_shield_time
        print(life)
        
        window.fill((0,0,0), (0, 0, 960, game_area_ulim))
        text_surface, rect = gamefont.render(f"LIVES = {life}", (0, 200, 200))
        pygame.draw.line(window, box_colour, (0, game_area_ulim-1), (960, game_area_ulim-1), 1)
        window.blit(text_surface, (20, 20))
    
# seperation * (inibars-1) -width - disp

while run:
    score += speed
    
    # GENERATE BOX AND REMOVE NON RENEDRED BOX   
    tx += speed
    if tx >= width + disp:
        ulim = random.randint(270-deviation, 270+deviation)
        kill_zone.pop(0)
        kill_zone.pop(0)
        kill_zone.append([seperation*ini_bars - width, game_area_ulim, width, ulim])
        kill_zone.append([seperation*ini_bars - width, ulim+gap+game_area_ulim, width, 540-ulim-gap])
        tx -= seperation
    
    # MOVE BOX BACK
    for coords in kill_zone:
        coords[0] -= speed
    
    # CHECK IF CLOSE BUTTON IS PRESSED, IF TRUE SET RUN = FALSE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    
    window.fill((0,0,0), (150, 0, 960, game_area_ulim))
    text_surface2, rect2 = gamefont.render(f"SCORE = {score//50}", (0, 200, 200))
    window.blit(text_surface2, (150, 20))
    pygame.draw.line(window, box_colour, (0, game_area_ulim-1), (960, game_area_ulim-1), 1)
    
    # CLEAR SCREEN AND RENDER BOXES PRESENT IN KILL_LIST
    window.fill((0,0,0), (0, 60, 960, 540+game_area_ulim-60))
    for j in kill_zone:
        pygame.draw.rect(window, box_colour, pygame.Rect(j))
    pygame.display.flip()

    # CHECK IF PLAYER IS IN KILLZONE AND DEAL DAMAGE IF PLAYER NOT INVINCIBLE
    if (check_if_in(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])) or pygame.mouse.get_pos()[1] < game_area_ulim:
        deal_dmg()
    
    
    
