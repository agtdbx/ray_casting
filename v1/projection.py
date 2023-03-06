import pygame as pg

class Projetcion:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.camera_rotate_speed = 2.5


    def draw(self, screen, views):
        pg.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 1)
        nb = 0
        dst_max = views[0][4]
        for view in views:
            if (view[3]):
                x = self.x + (nb / len(views)) * self.w
                large = self.w // len(views)
                y = self.y + self.h / 2
                size = ((dst_max - view[2]) / dst_max) * self.h
                top = y - size / 2
                bot = y + size / 2
                color = (dst_max - view[2]) / (dst_max / 255)
                pg.draw.line(screen, (color, color, color), (x, top), (x, bot), large)
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
