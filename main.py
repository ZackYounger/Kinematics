import time

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

#
class Limb:
    def __init__(self, bone_no=3):
        self.start_pos = [width / 2, height / 2]
        self.end_pos = []
        self.bone_no = bone_no
        self.bone_length = 100
        self.bones = [MainJoint(None, [width / 2, height / 2], True)]

        for bone in range(self.bone_no):
            self.bones.append(Bone(self.bones[bone].end_pos,
                                   [self.bones[bone].end_pos[0] + self.bone_length, self.bones[bone].end_pos[1]],
                                   self.bone_length))

        self.bones.append(MainJoint(self.bones[-1].end_pos, None, False))
        print(self.bones)

    def update(self):
        for bone in self.bones:
            bone.update()
        self.backward_adjust()
        self.forward_adjust()


    def draw(self):
        for bone in self.bones:
            bone.draw()

    def backward_adjust(self):
        self.bones = self.bones[::-1]
        for index, value in enumerate(self.bones[1:-1]):
            index = index + 1
            self.bones[index].end_pos = self.bones[index - 1].start_pos
            distance = sqrt((self.bones[index].start_pos[0] - self.bones[index].end_pos[0])**2 + (self.bones[index].start_pos[1] - self.bones[index].end_pos[1])**2)
            n_vector = [(self.bones[index].start_pos[0] - self.bones[index].end_pos[0]) / distance,
                        (self.bones[index].start_pos[1] - self.bones[index].end_pos[1]) / distance]    # [dx to dy]
            self.bones[index].start_pos = [self.bones[index].length * n_vector[0] + self.bones[index].end_pos[0],
                                           self.bones[index].length * n_vector[1] + self.bones[index].end_pos[1]]

            #time.sleep(1)
        self.bones = self.bones[::-1]

    def forward_adjust(self):
        for index, value in enumerate(self.bones[1:-1]):
            index = index + 1
            self.bones[index].start_pos = self.bones[index - 1].end_pos
            distance = sqrt((self.bones[index].end_pos[0] - self.bones[index].start_pos[0]) ** 2 + (
                        self.bones[index].end_pos[1] - self.bones[index].start_pos[1]) ** 2)
            n_vector = [(self.bones[index].end_pos[0] - self.bones[index].start_pos[0]) / distance,
                        (self.bones[index].end_pos[1] - self.bones[index].start_pos[1]) / distance]  # [dx to dy]
            self.bones[index].end_pos = [self.bones[index].length * n_vector[0] + self.bones[index].start_pos[0],
                                           self.bones[index].length * n_vector[1] + self.bones[index].start_pos[1]]


class MainJoint():
    def __init__(self, start_pos, end_pos, fixed):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.fixed = fixed

    def update(self):
        if not self.fixed:
            self.start_pos = mouse_pos

    def draw(self):
        pygame.draw.circle(screen, white, (round(self.end_pos[0]), round(self.end_pos[1])) if self.fixed else (round(self.start_pos[0]), round(self.start_pos[1])), 5)


class Bone:
    def __init__(self, start_pos, end_pos, length):
        self.colour = (rand(0, 255), rand(0, 255), rand(0, 255))
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.angle = pi / 2
        self.length = length

    def update(self):
        pass

    def draw(self):
        pygame.draw.line(screen, self.colour, self.start_pos, self.end_pos)


mouse_pos = pygame.mouse.get_pos()
l = Limb()


running = True
while running:
    clock.tick(fps_limit)
    screen.fill(background_colour)
    mouse_pos = pygame.mouse.get_pos()

    distance = sqrt((width/2 - mouse_pos[0])**2 + (height/2 - mouse_pos[1])**2)
    if distance > l.bone_no * l.bone_length:
        n_vector = [(mouse_pos[0] - height/2) / distance,
                    (mouse_pos[1] - height/2) / distance]
        mouse_pos = [l.bone_no * l.bone_length * n_vector[0] + height/2,
                     l.bone_no * l.bone_length * n_vector[1] + width/2]

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                l.update()

    l.update()
    l.draw()

    pygame.draw.circle(screen, white, (round(mouse_pos[0]), round(mouse_pos[1])), 10, 3)

    pygame.display.flip()
pygame.quit()
