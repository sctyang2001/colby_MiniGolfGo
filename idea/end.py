# CS 269 
# Chloe Zhang 
# End screen

import pygame

# initialize pygame
pygame.init()
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Golf Simulator")
clock = pygame.time.Clock()

# game variables
FPS = 30
font = pygame.font.Font('freesansbold.ttf', 42)

# set RGB of colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (4, 34, 16)# background greenish color

def main():
    run = True
    while run:
        WIN.fill(BG)
        end_text = font.render('Thanks for playing!', True, WHITE)
        WIN.blit(end_text, (450, 300))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #start fading out the screen
                sur = pygame.Surface((WIDTH, HEIGHT))
                sur.fill(BLACK)
                for alpha in range (0, 300):
                    sur.set_alpha(alpha)
                    WIN.blit(sur, (0,0))
                    pygame.display.flip()
                    pygame.time.delay(10)
                run = False
                pygame.quit()

main()