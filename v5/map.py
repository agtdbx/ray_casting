import pygame as pg

def init_map(w, h):
    my_map = []
    for y in range(0, h):
        lst = []
        for x in range(0, w):
            collision = 0
            if (y == 0 or y == h - 1 or x == 0 or x == w - 1):
                collision = 1
            lst.append(collision)
        my_map.append(lst)
    return my_map


def draw_map(my_map, screen, size):
    for y in range(0, len(my_map)):
        for x in range(0, len(my_map[0])):
            if (my_map[y][x] == 1):
                pg.draw.rect(screen, (30, 30, 30), (x * size, y * size, size, size))


def draw_highlight_map(my_map, screen, views, size):
    for view in views:
        tx = int(view[0] // size)
        ty = int(view[1] // size)
        if (view[3]):
            color = 255 - view[2] / 2
            if color < 30:
                color = 30
            pg.draw.rect(screen, (color, color, color), (tx * size, ty * size, size, size))


def clic_on_map(my_map, pos, mouse_state, hitbox, size):
    collision = 1
    if (mouse_state):
        collision = 0
    x = pos[0] // size
    y = pos[1] // size
    w = len(my_map[0])
    h = len(my_map)
    if ((x >= hitbox[0] and x <= hitbox[2]) and\
        (y >= hitbox[1] or y <= hitbox[3])):
        return
    if (y > 0 and y < h - 1 and x > 0 and x < w - 1):
        my_map[y][x] = collision
    return my_map


def load_map(strmap):
    my_map = []
    lst = []
    for i in range(0, len(strmap) - 1):
        c = strmap[i]
        if (c == '\n'):
            my_map.append(lst)
            lst = []
        else:
            lst.append(int(c))
    my_map.append(lst)

    return my_map


def get_save_map(my_map):
    res = ""
    for y in range(0, len(my_map)):
        for x in range(0, len(my_map[0])):
            res += str(my_map[y][x])
        res += '\n'
    return res
