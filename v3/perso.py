import math
import pygame as pg

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


    def walkable(self, x, y, map):
        ty1 = int((y - self.bloc_size) // self.bloc_size)
        ty2 = int((y + self.bloc_size * 2) // self.bloc_size)

        tx1 = int((x - self.bloc_size) // self.bloc_size)
        tx2 = int((x + self.bloc_size * 2) // self.bloc_size)
        for ty in range(ty1, ty2):
            for tx in range(tx1, tx2):
                if (map.is_collision(tx, ty)):
                        return False
        return True


    def input(self, map, delta, z, q, s, d):
        coef_x, coef_y = self.get_coef(self.rotation)
        coef_x *= self.speed * delta
        coef_y *= self.speed * delta

        if (z):
            if (self.walkable(self.x + coef_x, self.y, map)):
                self.x += coef_x
            if (self.walkable(self.x, self.y + coef_y, map)):
                self.y += coef_y

        elif (s):
            if (self.walkable(self.x - coef_x, self.y, map)):
                self.x -= coef_x
            if (self.walkable(self.x, self.y - coef_y, map)):
                self.y -= coef_y

        if (q):
            if (self.walkable(self.x + coef_y, self.y, map)):
                self.x += coef_y
            if (self.walkable(self.x, self.y - coef_x, map)):
                self.y -= coef_x

        elif (d):
            if (self.walkable(self.x - coef_y, self.y, map)):
                self.x -= coef_y
            if (self.walkable(self.x, self.y + coef_x, map)):
                self.y += coef_x


    def get_hitbox(self):
        return (self.x, self.y, self.x + self.size, self.y + self.size)


    def get_coef(self, rotation):
        radians = rotation * (math.pi / 180)
        return (math.cos(radians), math.sin(radians))


    def draw_ray(self, map):
        self.views = []
        champ_vision = 60
        nb_rayon = 192
        precisionDegree = champ_vision / nb_rayon
        distance_max = 675
        precisionDistance = 3
        for i in range(-(nb_rayon // 2), (nb_rayon // 2) + 1):
            x = self.x
            y = self.y
            tx = int(x // self.bloc_size)
            ty = int(y // self.bloc_size)
            dist = 0

            rot = self.rotation + (precisionDegree * i)
            coefs = self.get_coef(rot)

            coef_x = coefs[0]
            coef_y = coefs[1]

            while (not map.is_collision(tx, ty) and dist <= distance_max):
                x += precisionDistance * coef_x
                y += precisionDistance * coef_y
                tx = int(x // self.bloc_size)
                ty = int(y // self.bloc_size)
                dist = math.dist((self.x, self.y), (x, y))

            if dist <= distance_max:
                while (map.is_collision(tx, ty) and dist <= distance_max):
                    x -= 1 * coef_x
                    y -= 1 * coef_y
                    tx = int(x // self.bloc_size)
                    ty = int(y // self.bloc_size)
                    dist = math.dist((self.x, self.y), (x, y))
                x += 1 * coef_x
                y += 1 * coef_y
                tx = int(x // self.bloc_size)
                ty = int(y // self.bloc_size)
                dist = math.dist((self.x, self.y), (x, y))

            self.views.append((x, y, dist, dist <= distance_max, rot, map.get_color(tx, ty, x, y)))


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
