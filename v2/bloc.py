import pygame as pg

class Bloc:
    def __init__(self, collision, x, y, size):
        self.collision = collision
        self.x = x * size
        self.y = y * size
        self.size = size
        self.hitbox = (self.x, self.y, self.size, self.size)


    def draw(self, screen):
        if (self.collision):
            pg.draw.rect(screen, (30, 30, 30), self.hitbox)


    def draw_highlight(self, screen, view):
        if (view[3]):
            color = 255 - view[2] / 2
            if color < 30:
                color = 30
            pg.draw.rect(screen, (color, color, color), self.hitbox)

    def is_collision(self):
        return (self.collision)

    def get_color(self, x, y):
        precision = 1
        if (abs(x - self.x) <= precision and y >= self.y and y <= self.y + self.size):
            return (50, 140, 245)
        if (abs(x - (self.x + self.size)) <= precision and y >= self.y and y <= self.y + self.size):
            return (50, 140, 245)
        if (x >= self.x and x <= self.x + self.size and abs(y - self.y) <= precision):
            return (50, 150, 255)
        if (x >= self.x and x <= self.x + self.size and abs(y - (self.y + self.size)) <= precision):
            return (50, 150, 255)
        return (255, 100, 100)
