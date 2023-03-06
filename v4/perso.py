import math
import time
import pygame as pg
from numba import njit
from numba.typed import List


@njit(fastmath=True)
def ray(ox, oy, bloc_size, distance_max, map, start_rot, precisionDistance, precisionDegree, i):
    x = ox
    y = oy
    tx = int(x // bloc_size)
    ty = int(y // bloc_size)
    dist = 0

    rot = start_rot + (precisionDegree * i)
    radians = rot * (math.pi / 180)
    coefs = (math.cos(radians), math.sin(radians))

    coef_x = coefs[0]
    coef_y = coefs[1]

    while (map[ty][tx] == 0 and dist <= distance_max):
        x += precisionDistance * coef_x
        y += precisionDistance * coef_y
        tx = int(x // bloc_size)
        ty = int(y // bloc_size)
        dist = math.sqrt((ox - x)**2 + (oy - y)**2)

    if dist <= distance_max:
        while (map[ty][tx] == 1 and dist <= distance_max):
            x -= 0.01 * coef_x
            y -= 0.01 * coef_y
            tx = int(x // bloc_size)
            ty = int(y // bloc_size)
            dist = math.sqrt((ox - x)**2 + (oy - y)**2)
        x += 0.01 * coef_x
        y += 0.01 * coef_y
        tx = int(x // bloc_size)
        ty = int(y // bloc_size)
        dist = math.sqrt((ox - x)**2 + (oy - y)**2)

    return (x, y, dist, rot)


class Perso:
    def __init__(self, x, y, size, bloc_size):
        self.x = x
        self.y = y
        self.size = size
        self.bloc_size = bloc_size
        self.speed = 150
        self.speed_rot = 180
        self.rotation = 0
        self.views = [(0, 0)]


    def draw(self, screen, draw_lines = False, draw_all_line = False):
        if (draw_lines):
            for view in self.views:
                if (view[3] or draw_all_line):
                    pg.draw.line(screen, (255, 255, 255), (self.x, self.y), (view[0], view[1]))
        pg.draw.circle(screen, (200, 100, 100), (self.x, self.y), self.size * 1.5)


    def walkable(self, x, y, my_map):
        ty1 = int((y - self.bloc_size) // self.bloc_size)
        ty2 = int((y + self.bloc_size * 2) // self.bloc_size)

        tx1 = int((x - self.bloc_size) // self.bloc_size)
        tx2 = int((x + self.bloc_size * 2) // self.bloc_size)
        for ty in range(ty1, ty2):
            for tx in range(tx1, tx2):
                if (my_map[ty][tx]):
                        return False
        return True


    def input(self, my_map, delta, z, q, s, d):
        coef_x, coef_y = self.get_coef(self.rotation)
        coef_x *= self.speed * delta
        coef_y *= self.speed * delta

        if (z):
            if (self.walkable(self.x + coef_x, self.y, my_map)):
                self.x += coef_x
            if (self.walkable(self.x, self.y + coef_y, my_map)):
                self.y += coef_y

        elif (s):
            if (self.walkable(self.x - coef_x, self.y, my_map)):
                self.x -= coef_x
            if (self.walkable(self.x, self.y - coef_y, my_map)):
                self.y -= coef_y

        if (q):
            if (self.walkable(self.x + coef_y, self.y, my_map)):
                self.x += coef_y
            if (self.walkable(self.x, self.y - coef_x, my_map)):
                self.y -= coef_x

        elif (d):
            if (self.walkable(self.x - coef_y, self.y, my_map)):
                self.x -= coef_y
            if (self.walkable(self.x, self.y + coef_x, my_map)):
                self.y += coef_x


    def get_hitbox(self):
        return (self.x, self.y, self.x + self.size, self.y + self.size)


    def get_coef(self, rotation):
        radians = rotation * (math.pi / 180)
        return (math.cos(radians), math.sin(radians))


    def draw_ray(self, my_map):
        self.views = []
        champ_vision = 70
        nb_rayon = 192 * 5
        precisionDegree = champ_vision / nb_rayon
        distance_max = 675
        precisionDistance = 1

        cx, cy = self.get_coef(self.rotation)

        px = self.x - cx * (self.size)
        py = self.y - cy * (self.size)

        accelerate_map = List()
        for l in my_map:
            li = List()
            for i in l:
                li.append(i)
            accelerate_map.append(li)

        start_rot = self.rotation + (precisionDegree * -(nb_rayon // 2))

        for i in range(nb_rayon):
            x, y, dist, rot = ray(px, py, self.bloc_size, distance_max, accelerate_map, start_rot, precisionDistance, precisionDegree, i)

            mx = x % self.size
            my = y % self.size

            precision = 0.01

            if (mx <= precision or self.size - mx <= precision):
                self.views.append((x, y, dist, dist <= distance_max, rot, (50, 150, 255)))
            elif (self.size - my <= precision or my <= precision):
                self.views.append((x, y, dist, dist <= distance_max, rot, (40, 140, 245)))
            else:
                self.views.append((x, y, dist, dist <= distance_max, rot, (255, 0, 0)))


    def get_views(self):
        return self.views


    def get_rotation(self):
        return self.rotation


    def add_rotation(self, value):
        self.rotation += value
        if (self.rotation > 180):
            self.rotation -= 360
        if (self.rotation < -180):
            self.rotation += 360
