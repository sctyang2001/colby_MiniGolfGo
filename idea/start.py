# CS 269
# Chloe Zhang
# Starting screen

import pygame
from pygame import mixer
import os
import sys
import game

# initialize pygame
pygame.init()
#load music
mixer.init()
mixer.music.load('../audios/BGM_startingGame_LoveDream.mp3')
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Hole In One")
clock = pygame.time.Clock()

# game variables
FPS = 30
font = pygame.font.SysFont('Verdana', 45)

# set RGB of colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (248, 249, 212)# background yellow

#read and transform images needed
start_ori = pygame.image.load(os.path.join('../pictures', 'startScreen.png'))
start_img = pygame.transform.scale(start_ori, (796,465))
ball_ori = pygame.image.load(os.path.join('../pictures', 'ball_yellowbg.png')).convert()
ball_img = pygame.transform.scale(ball_ori, (200,200))
ball_img.set_colorkey(-1, pygame.RLEACCEL)

#tutorial png
rule_1 = pygame.image.load(os.path.join('../rules', 'game_rule.png'))
rule_2 = pygame.image.load(os.path.join('../rules', 'game_items.png'))
rule_3 = pygame.image.load(os.path.join('../rules', 'level_editor_rule.png'))



def tutorial():
    fadeOut(1280, 720, BG)
    WIN.blit(rule_1, (0,0))
    pygame.display.flip()
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.time.wait(100)
                wait = False
            elif event.type == pygame.WINDOWCLOSE :
                sys.exit()
    fadeOut(1280, 720, BLACK)
    fadeOut(1280, 720, BG)
    
    WIN.blit(rule_2, (0,0))
    pygame.display.flip()
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.time.wait(100)
                wait = False
            elif event.type == pygame.WINDOWCLOSE :
                sys.exit()
    fadeOut(1280, 720, BLACK)
    fadeOut(1280, 720, BG)
   
    WIN.blit(rule_3, (0,0))
    pygame.display.flip()
    wait = True    
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.time.wait(100)
                wait = False
            elif event.type == pygame.WINDOWCLOSE :
                sys.exit()
    fadeOut(1280, 720, BLACK)
    fadeOut(1280, 720, BG)

#fade out function used to fade out a selected area
def fadeOut(width, height, color):
    sur = pygame.Surface((width, height)).convert_alpha()
    sur.fill(color)

    for alpha in range (0, 165):
        sur.set_alpha(alpha//10)
        WIN.blit(sur, (0,0),special_flags=pygame.BLEND_ALPHA_SDL2)
        pygame.display.flip()
        # pygame.time.wait(10)

#rotate the ball and blit the img with its new position
def blitRotateBall(win, img):
    angle = 0
    loop = True
    while loop:
        angle += 6
        win.fill(BG)
        start_text = font.render('Click to Start', True, BLACK)
        WIN.blit(start_text, (WIDTH//2-start_text.get_width()//2, HEIGHT//4-start_text.get_height()//2))
        mx, my = pygame.mouse.get_pos()
        img_copy = pygame.transform.rotate(img, angle)
        img_copy.set_colorkey(BG)
        win.blit(img_copy, (mx - int(img.get_width() / 2), my - int(img.get_height() / 2)),pygame.Rect(img.get_width()//2-30,img.get_height()//2-30,100,100))
        pygame.display.flip()
        pygame.time.wait(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                loop = False
            # elif event.type == pygame.WINDOWCLOSE :
                # sys.exit()

def interface():
    #start music
    mixer.music.play()
    WIN.fill(BG)
    pygame.display.flip()
    pygame.time.wait(100)

    #displaying start image
    WIN.blit(start_img,(242,79))
    pygame.display.flip()
    pygame.time.wait(3000)

    #fading out the start image
    fadeOut(1280, 720, BG)
        
    # blit the text onto the screen
    start_text = font.render('Click to Start', True, BLACK)
    WIN.blit(start_text, (WIDTH//2-start_text.get_width()//2, HEIGHT//2+start_text.get_height()//2))
    pygame.display.flip()

    #rotate and move ball image
    blitRotateBall(WIN, ball_img)

    #set up click to start game play and text disappearance
    fadeOut(1280, 720, BLACK)
    tutorial()


def main():
    run = True
    # while run:
        # for event in pygame.event.get():
            # if event.type == pygame.QUIT:
                # run = False
                # pygame.quit()
    interface()
    
    mixer.music.stop()
    game.main(sys.argv)

main()