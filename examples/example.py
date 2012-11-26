# coding: utf-8

import time
import random

from pattern import switch

class Cell(object):
    ALIVE = True
    DEAD = False

    def __init__(self, state=DEAD):
        self.state = state
        self.next_state = Cell.DEAD
        self.neighbors = []

    def tick(self):
        self.state = self.next_state

    def live(self):
        self.state = Cell.ALIVE

    def die(self):
        self.state = Cell.DEAD

class LifeGame(object):
    NEIGHBORS = [
        (-1, -1), ( 0, -1), (1, -1),
        (-1,  0),           (1,  0),
        (-1,  1), ( 0,  1), (1,  1),
    ]
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.create_cells()
        self.bind_cells()

    def create_cells(self):
        self.cells = {}
        for x in range(self.w):
            for y in range(self.h):
                self.cells[(x, y)] = Cell()

    def bind_cells(self):
        for x, y in self.cells:
            cell = self.cells[(x, y)]
            for dx, dy in LifeGame.NEIGHBORS:
                n = self.cells.get((x + dx, y + dy), None)
                if n:
                    cell.neighbors.append(n)

    def next(self):
        for cell in self.cells.values():
            count = len(filter(lambda c: c.state == Cell.ALIVE, cell.neighbors))
            cell.next_state = switch(
                count,
                2, cell.state,
                3, Cell.ALIVE,
                Cell.DEAD)
        for cell in self.cells.values():
            cell.tick()


    def show(self):
        s = ''
        for y in range(self.h):
            for x in range(self.w):
                s += u'*' if self.cells[(x, y)].state else u'_'
            s += '\n'
        return s

    def reset(self, cells=[]):
        for y, l in enumerate(cells):
            for x, c in enumerate(l):
                switch(c,
                       '_', lambda: self.cells[(x, y)].die(),
                       '*', lambda: self.cells[(x, y)].live(),
                       '*', lambda: self.cells.__setitem__((x, y), Cell.ALIVE))


class LifeGameFn(object):
    NEIGHBORS = [
        (-1, -1), ( 0, -1), (1, -1),
        (-1,  0),           (1,  0),
        (-1,  1), ( 0,  1), (1,  1),
    ]
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.create_cells()
        self.bind_cells()

    def create_cells(self):
        self.cells = {}
        for x in range(self.w):
            for y in range(self.h):
                self.cells[(x, y)] = Cell()

    def bind_cells(self):
        for x, y in self.cells:
            cell = self.cells[(x, y)]
            for dx, dy in LifeGame.NEIGHBORS:
                n = self.cells.get((x + dx, y + dy), None)
                if n:
                    cell.neighbors.append(n)

    def next(self):
        for cell in self.cells.values():
            count = len(filter(lambda c: c.state == Cell.ALIVE, cell.neighbors))
            cell.next_state = switch(
                count,
                2, cell.state,
                3, Cell.ALIVE,
                Cell.DEAD)
        for cell in self.cells.values():
            cell.tick()


    def show(self):
        s = ''
        for y in range(self.h):
            for x in range(self.w):
                s += u'*' if self.cells[(x, y)].state else u'_'
            s += '\n'
        return s

    def reset(self, cells=[]):
        for y, l in enumerate(cells):
            for x, c in enumerate(l):
                switch(c,
                       '_', lambda: self.cells[(x, y)].die(),
                       '*', lambda: self.cells[(x, y)].live(),
                       '*', lambda: self.cells.__setitem__((x, y), Cell.ALIVE))


def main():
    game = LifeGame(40, 20)
    game.cells[(2,0)].state = Cell.ALIVE
    game.cells[(2,1)].state = Cell.ALIVE
    game.cells[(2,2)].state = Cell.ALIVE
    game.cells[(1,2)].state = Cell.ALIVE
    game.cells[(0,1)].state = Cell.ALIVE

    for i in range(400):
        game.cells[(random.randint(0, game.w - 1), random.randint(0, game.h - 1))].state = Cell.ALIVE

    while(True):
        print "=================================="
        print game.show()
        game.next()

if __name__=='__main__':
    main()
