import pygame
from math import *
from random import randint as rand

pygame.init()

clock = pygame.time.Clock()
fps_limit = 30

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
background_colour = black

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)


class Limb:
    def __init__(self, bone_no = 3):
        self.start_pos = [width/2, height/2]
        self.end_pos = []
        self.bone_no = bone_no
        self.bone_length = 70
        self.bones = [MainJoint([width/2, height/2])]

        for bone in range(self.bone_no):
            self.bones.append(Bone(self.bones[bone].end_pos, [self.bones[bone].end_pos[0] + self.bone_length, self.bones[bone].end_pos[1]], self.bone_length))

    def update(self):
        for bone in self.bones:
            bone.update()

    def forward_adjust(self):
        pass

    def backward_adjust(self):
        pass


class MainJoint():
    def __init__(self, pos):
        self.end_pos = pos

    def update(self):
        pass


class Bone:
    def __init__(self, start_pos, end_pos, length):
        self.colour = (rand(0, 255), rand(0, 255), rand(0, 255))
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.angle = pi/2
        self.length = length

    def update(self):
        pygame.draw.line(screen, self.colour, self.start_pos, self.end_pos)

l = Limb()

running = True
while running:
    clock.tick(fps_limit)
    screen.fill(background_colour)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    l.update()

    pygame.display.flip()
pygame.quit()
