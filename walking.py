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

ground_level = height - 50

g = 2

tick = 0


class Limb:
    def __init__(self, bone_no=3, start_pos=[width / 2, height / 2]):
        self.start_pos = start_pos
        self.end_pos = []
        self.bone_no = bone_no
        self.bone_length = 30
        self.bones = [MainJoint(None, [width / 2, height / 2], True)]
        self.t = 1

        for bone in range(self.bone_no):
            self.bones.append(Bone(self.bones[bone].end_pos,
                                   [self.bones[bone].end_pos[0] + self.bone_length, self.bones[bone].end_pos[1]],
                                   self.bone_length))

        self.bones.append(MainJoint(self.bones[-1].end_pos, None, False))
        self.saved_end_point = [start_pos[0], ground_level]

    def update(self, start_pos):
        temp_value = self.saved_end_point[0] - body.pos[0]

        if abs(temp_value) > body.step_size and self.t >= 1:
            self.t = 0

        if self.t == 0:
            self.p0 = [self.saved_end_point[0], ground_level]
            self.p1 = [body.pos[0], ground_level - body.step_height]
            self.p2 = [body.pos[0] - body.step_size * (temp_value / abs(temp_value)) * 1.5, ground_level]

        if self.t < 1:
            self.t += 0.1
            self.saved_end_point = [self.p0[0]*(self.t**2 - 2*self.t + 1) + self.p1[0]*(-2*self.t**2 + 2*self.t) + self.p2[0]*(self.t**2),
                                    self.p0[1]*(self.t**2 - 2*self.t + 1) + self.p1[1]*(-2*self.t**2 + 2*self.t) + self.p2[1]*(self.t**2)]
            #pygame.draw.circle(screen, red, self.p0, 3)
            #pygame.draw.circle(screen, red, self.p1, 3)
            #pygame.draw.circle(screen, red, self.p2, 3)


        #if abs(temp_value) > body.step_size:
        #    self.saved_end_point[0] = body.pos[0] - body.step_size * (temp_value / abs(temp_value))


        self.bones[0].end_pos = start_pos

        #self.bones[-1].start_pos = [start_pos[0] + rand(-1,1), ground_level]
        self.bones[-1].start_pos = self.saved_end_point

        for bone in self.bones:
            bone.update(self)
        for i in range(9):
            self.backward_adjust()
            self.forward_adjust()
        self.draw()

    def draw(self):
        for bone in self.bones:
            bone.draw()

    def backward_adjust(self):
        self.bones = self.bones[::-1]
        for index, value in enumerate(self.bones[1:-1]):
            index = index + 1
            self.bones[index].end_pos = self.bones[index - 1].start_pos
            distance = sqrt((self.bones[index].start_pos[0] - self.bones[index].end_pos[0]) ** 2 + (
                    self.bones[index].start_pos[1] - self.bones[index].end_pos[1]) ** 2)
            n_vector = [(self.bones[index].start_pos[0] - self.bones[index].end_pos[0]) / distance,
                        (self.bones[index].start_pos[1] - self.bones[index].end_pos[1]) / distance]  # [dx to dy]
            self.bones[index].start_pos = [self.bones[index].length * n_vector[0] + self.bones[index].end_pos[0],
                                           self.bones[index].length * n_vector[1] + self.bones[index].end_pos[1]]

            # time.sleep(1)
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


class MainJoint:
    def __init__(self, start_pos, end_pos, fixed):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.fixed = fixed

    def update(self, leg_data):
        if not self.fixed and len(leg_data.end_pos) != 0:
            self.start_pos = [leg_data.end_pos[0], ground_level]

    def draw(self):
        pygame.draw.circle(screen, white, (round(self.end_pos[0]), round(self.end_pos[1])) if self.fixed else (
            round(self.start_pos[0]), round(self.start_pos[1])), 5)


class Bone:
    def __init__(self, start_pos, end_pos, length):
        self.colour = (rand(0, 255), rand(0, 255), rand(0, 255))
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.angle = pi / 2
        self.length = length

    def update(self, leg_data):
        pass

    def draw(self):
        pygame.draw.line(screen, self.colour, self.start_pos, self.end_pos)


class Body:
    def __init__(self, no_legs=2, pos=[width / 2, 600]):
        self.width = 30
        self.height = 60
        self.no_legs = no_legs
        self.pos = pos
        self.vel = [0, 0]
        self.force = [0, 0]
        self.acc = [0, 0]
        self.drag = 0.98
        self.legs = [Limb(3, [self.pos[0] - self.width / 2 + self.width / (self.no_legs - 1) * leg, self.pos[1] + self.height / 2])
                     for leg in range(self.no_legs)]
        self.mass = 10
        self.step_size = 35
        self.step_height = 50

    def update(self):
        self.reaction_force = 0
        self.horizontal_force = 0
        for leg in self.legs:
            if ground.collidepoint(leg.bones[-2].end_pos):
                self.reaction_force += (ground_level - (self.legs[0].bone_length * self.legs[0].bone_no))**1.5 * 0.0002

            self.horizontal_force += ((leg.bones[-2].end_pos[0] - self.pos[0]))

        self.force = [self.horizontal_force, g - self.reaction_force]

        self.acc = [self.force[0]/self.mass, self.force[1]/self.mass]

        if keys[pygame.K_LEFT]:
            self.vel[0] = -10
        if keys[pygame.K_RIGHT]:
            self.vel[0] = 10

        self.vel = [self.vel[0] + self.acc[0], self.vel[1] + self.acc[1]]
        self.vel = [self.vel[0] * self.drag * 0.5, self.vel[1] * self.drag]
        self.pos = [self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]]

        for index, leg in enumerate(self.legs):
            leg.update([self.pos[0] - self.width / 2 + self.width / (self.no_legs - 1) * index, self.pos[1] + self.height / 2])

        self.draw()

    def draw(self):
        pygame.draw.rect(screen, white, [round(self.pos[0] - self.width / 2), round(self.pos[1] - self.height / 2), self.width, self.height])


mouse_pos = pygame.mouse.get_pos()
body = Body()

running = True
while running:
    clock.tick(fps_limit)
    tick += 1
    screen.fill(background_colour)
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw ground
    ground = pygame.Rect(0, ground_level, width, height - ground_level)
    pygame.draw.rect(screen, (150, 150, 150), ground)

    body.update()

    pygame.display.flip()
pygame.quit()
