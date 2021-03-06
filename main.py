import pygame as pg

pg.init()

screen = pg.display.set_mode((800, 800))

black = (0, 0, 0)
white = (255, 255, 255)
fake_white = (220, 200, 200)

screen.fill(black)

case = 5


def make_grid():
    for i in range(160):
        pg.draw.line(screen, fake_white, (i * case, 0), (i * case, 800), 1)
        pg.draw.line(screen, fake_white, (0, i * case), (800, i * case), 1)
    pg.draw.line(screen, fake_white, (799, 0), (799, 799), 1)
    pg.draw.line(screen, fake_white, (0, 799), (799, 799))


def get_start(x):
    i = 0
    j = 0
    while i < x - 5:
        i += 5
        j += 1
    return j * 5 + 1


class Make_rect:

    def __init__(self, x, y):
        self.x = get_start(x)
        self.y = get_start(y)
        self.life = black
        self.next = None

    def set_rect(self):
        return pg.Rect(self.x, self.y, 4, 4)

    def get_next(self):
        if self.life == white:
            count = -1
        else:
            count = 0
        start_y = self.y - 5
        for _ in range(3):
            start_x = self.x - 5
            for _ in range(3):
                try:
                    if pg.Surface.get_at(screen, (start_x, start_y)) == white:
                        count += 1
                        if count > 3:
                            return count
                except IndexError:
                    pass
                start_x += 5
            start_y += 5
        return count


l_case = []
base_cas = True
running = True


def create_obj():
    for i in range(160):
        for j in range(160):
            l_case.append(Make_rect(j * 5 + 1, i * 5 + 1))

    for i in l_case:
        pg.draw.rect(screen, black, i.set_rect())


create_obj()


def main():

    global running, base_cas, l_case

    count = 0

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    l_case = []
                    base_cas = True
                    screen.fill(black)
                    create_obj()
                    count = 0
                elif event.key == pg.K_c:
                    print(count)
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
            for c in range(len(l_case)):
                pg.draw.rect(screen, l_case[c].life, l_case[c].set_rect())
            for c in l_case:
                if c.next is not None:
                    c.life = c.next
            count += 1
        make_grid()
        pg.display.update()


if __name__ == '__main__':
    main()
