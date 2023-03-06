import math
import pygame as pg

class Perso:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = 250
        self.speed_rot = 180
        self.rotation = 0
        self.views = [(0, 0)]
        self.draw_all_line = False


    def draw(self, screen, draw_lines = False, draw_all_line = False):
        self.draw_all_line = draw_all_line
        if (draw_lines):
            for view in self.views:
                if (view[3] or draw_all_line):
                    pg.draw.line(screen, (255, 255, 255), (self.x, self.y), (view[0], view[1]))
        pg.draw.circle(screen, (200, 100, 100), (self.x, self.y), self.size)


    def walkable(self, x, y, map):
        ty1 = int((y - self.size) // self.size)
        ty2 = int((y + self.size * 2) // self.size)

        tx1 = int((x - self.size) // self.size)
        tx2 = int((x + self.size * 2) // self.size)
        for ty in range(ty1, ty2):
            for tx in range(tx1, tx2):
                if (map.is_collision(tx, ty)):
                        return False
        return True


    def input(self, map, delta, z, q, s, d, mouse_pos):
        coef_x, coef_y = self.get_coef(self.rotation)
        coef_x *= self.speed * delta
        coef_y *= self.speed * delta

        if (z and self.walkable(self.x + coef_x, self.y + coef_y, map)):
            self.x += coef_x
            self.y += coef_y
        elif (s and self.walkable(self.x - coef_x, self.y - coef_y, map)):
            self.x -= coef_x
            self.y -= coef_y

        if (q and self.walkable(self.x + coef_y, self.y - coef_x, map)):
            self.x += coef_y
            self.y -= coef_x
        elif (d and self.walkable(self.x - coef_y, self.y + coef_x, map)):
            self.x -= coef_y
            self.y += coef_x

        """mouse_x, mouse_y = mouse_pos
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        self.rotation = (180 / math.pi) * math.atan2(rel_y, rel_x)"""


    def get_hitbox(self):
        return (self.x - self.size, self.y - self.size, self.x + self.size * 2, self.y + self.size * 2)


    def get_coef(self, rotation):
        radians = rotation * (math.pi / 180)
        return (math.cos(radians), math.sin(radians))


    def view_ray(self, map):
        self.views = []
        champ_vision = 80
        nb_rayon = 160
        precisionDegree = champ_vision / nb_rayon
        distance_max = 755
        precisionDistance = 15
        for i in range(-(nb_rayon // 2), (nb_rayon // 2) + 1):
            x = self.x
            y = self.y
            tx = int(x // self.size)
            ty = int(y // self.size)
            dist = 0

            rot = self.rotation + (precisionDegree * i)
            if (rot > 180):
                rot -= 360
            if (rot < -180):
                rot += 360
            coefs = self.get_coef(rot)

            coef_x = coefs[0]
            coef_y = coefs[1]

            while (not map.is_collision(tx, ty) and dist <= distance_max):
                x += precisionDistance * coef_x
                y += precisionDistance * coef_y
                tx = int(x // self.size)
                ty = int(y // self.size)
                dist = math.sqrt((self.x - x)**2 + (self.y - y)**2) - self.size

            self.views.append((x, y, dist, dist <= distance_max, distance_max))


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
