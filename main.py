import pygame as pg

pg.init()

screen = pg.display.set_mode((800, 800))

black = (0, 0, 0)
white = (255, 255, 255)
fake_white = (220, 200, 200)

screen.fill(black)

case = 20


def make_grid():
    for i in range(40):
        pg.draw.line(screen, fake_white, (i * case, 0), (i * case, 800), 1)
        pg.draw.line(screen, fake_white, (0, i * case), (800, i * case), 1)
    pg.draw.line(screen, fake_white, (799, 0), (799, 799), 1)
    pg.draw.line(screen, fake_white, (0, 799), (799, 799))


def get_start(x):
    i = 0
    j = 0
    while i < x - 20:
        i += 20
        j += 1
    return j * 20 + 1


class Make_rect:

    def __init__(self, x, y):
        self.x = get_start(x)
        self.y = get_start(y)
        self.life = black
        self.next = None
        if self.x == 1 or self.x == 781 or self.y == 1 or self.y == 781:
            if (self.x == 1 and self.y == 1) or (self.x == 1 and self.y == 781) or (self.x == 781 and self.y == 1) or (
                    self.x == 781 and self.y == 781):
                self.ex = 1
            else:
                self.ex = 2
        else:
            self.ex = 3

    def set_rect(self):
        return pg.Rect(self.x, self.y, 19, 19)

    def get_next(self):
        if self.life == white:
            count = -1
        else:
            count = 0
        start_y = self.y - 20
        for _ in range(3):
            start_x = self.x - 20
            for _ in range(3):
                try:
                    if pg.Surface.get_at(screen, (start_x, start_y)) == white:
                        count += 1
                        if count > 3:
                            return count
                except IndexError:
                    pass
                start_x += 20
            start_y += 20
        return count


l_case = []
base_cas = True
running = True

for i in range(40):
    for j in range(40):
        l_case.append(Make_rect(j * 20 + 1, i * 20 + 1))

for i in l_case:
    pg.draw.rect(screen, black, i.set_rect())
l_copy = l_case.copy()

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if base_cas:
            if event.type == pg.MOUSEBUTTONUP:
                x, y = event.pos
                x = get_start(x)
                y = get_start(y)
                for c in range(len(l_case)):
                    if x == l_case[c].x and y == l_case[c].y:
                        l_case[c] = Make_rect(x, y)
                        l_case[c].life = white
                        pg.draw.rect(screen, l_case[c].life, l_case[c].set_rect())
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    base_cas = False
        if not base_cas:
            for c in l_case:
                if c.life == black and c.get_next() == 3:
                    c.next = white
                elif c.life == white and (c.get_next() < 2 or c.get_next() > 3):
                    c.next = black
            screen.fill(black)
            pg.time.delay(100)
            for c in range(len(l_case)):
                pg.draw.rect(screen, l_case[c].life, l_case[c].set_rect())
            for c in l_case:
                if c.next is not None:
                    c.life = c.next
    make_grid()
    pg.display.update()
