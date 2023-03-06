import bloc as bloc

class Map:
    def __init__(self, size):
        self.w = 0
        self.h = 0
        self.map = []
        self.size = size


    def init_map(self, w, h):
        self.map = []
        self.w = w
        self.h = h
        for y in range(0, h):
            lst = []
            for x in range(0, w):
                collision = 0
                if (y == 0 or y == h - 1 or x == 0 or x == w - 1):
                    collision = 1
                lst.append(bloc.Bloc(collision, x, y, self.size))
            self.map.append(lst)


    def load_map(self, strmap):
        map = []
        lst = []
        for i in range(0, len(strmap) - 1):
            c = strmap[i]
            if (c == '\n'):
                map.append(lst)
                lst = []
            else:
                lst.append(int(c))
        map.append(lst)
        self.map = []
        self.w = len(map[0])
        self.h = len(map)
        for y in range(0, self.h):
            lst = []
            for x in range(0, self.w):
                lst.append(bloc.Bloc(map[y][x], x, y, self.size))
            self.map.append(lst)


    def draw(self, screen):
         for y in range(0, self.h):
            for x in range(0, self.w):
                self.map[y][x].draw(screen)


    def draw_highlight(self, screen, views):
        for view in views:
            tx = int(view[0] // 20)
            ty = int(view[1] // 20)
            self.map[ty][tx].draw_highlight(screen, view)


    def clic(self, pos, mouse_state, hitbox):
        collision = 1
        if (mouse_state):
            collision = 0
        x = pos[0]//20
        y = pos[1]//20
        if ((x >= hitbox[0] and x <= hitbox[2]) and\
            (y >= hitbox[1] or y <= hitbox[3])):
            return
        if (y > 0 and y < self.h - 1 and x > 0 and x < self.w - 1):
            self.map[y][x] = bloc.Bloc(collision, x, y, self.size)


    def is_collision(self, x, y):
        if (y > 0 and y < self.h - 1 and x > 0 and x < self.w - 1):
            return self.map[y][x].is_collision()
        return (True)


    def get_save_map(self):
        res = ""
        for y in range(0, self.h):
            for x in range(0, self.w):
                res += str(self.map[y][x].is_collision())
            res += '\n'
        return res


    def get_color(self, tx, ty, x, y):
        if (ty >= 0 and ty <= self.h - 1 and tx >= 0 and tx <= self.w - 1):
            return self.map[ty][tx].get_color(x, y)
        return (100, 255, 100)
