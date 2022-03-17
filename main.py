import pygame
from math import *
from random import randint as rand

pygame.init()

clock = pygame.time.Clock()
fps_limit = 30

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
background_colour = (0,0,0)

width,height = 800,800
screen = pygame.display.set_mode((width,height))
screen.fill(background_colour)

running = True
while running:
    clock.tick(fps_limit)
    screen.fill(background_colour)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()