import pygame as pg
import math

class Projetcion:
    def __init__(self, x, y, w, h, size):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.camera_rotate_speed = 2.5
        self.size = size


    def draw(self, screen, views, direction):
        pg.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 1)
        nb = 0
        for i in range(self.h // 2):
            color = (1 - (i / self.h)) / 2
            if (color < 0):
                color = 0
            pg.draw.rect(screen, (70 * color, 70 * color, 70 * color), (self.x, self.y + i, self.w, 1))
        for i in range(self.h // 2):
            color = (i / self.h) * 2
            pg.draw.rect(screen, (70 * color, 70 * color, 70 * color), (self.x, self.y + (self.h / 2) + i, self.w, 1))

        for view in views:
            rot = view[4] - direction
            radians = rot * (math.pi / 180)
            dist = view[2] * math.cos(radians)
            x = self.x + (nb / len(views)) * self.w
            large = (self.w // len(views)) + 1
            y = self.y + self.h / 2
            size = 24000 / dist
            top = y - size
            bot = y + size
            fog_force = 1024
            light = (fog_force - (view[2]*1.5)) / fog_force
            if (light < 0):
                light = 0
            color = view[5]
            pg.draw.line(screen, (color[0] * light, color[1] * light, color[2] * light), (x, top), (x, bot), large)
            nb += 1


    def rotate_camera(self, mouse_pos, perso, keys):
        x = mouse_pos[0]
        y = mouse_pos[1]
        mx = self.x + self.w / 2
        if (x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h):
            pg.mouse.set_visible(False)
            if (x > mx):
                perso.add_rotation(self.camera_rotate_speed)
            elif (x < mx):
                perso.add_rotation(-self.camera_rotate_speed)
            pg.mouse.set_pos(self.x + self.w / 2, self.y + self.h / 2)
            if (keys[pg.K_ESCAPE]):
                pg.mouse.set_pos(self.x - 20, self.y + self.h  + 20)
        else:
            pg.mouse.set_visible(True)
