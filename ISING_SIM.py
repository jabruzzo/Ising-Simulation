# Program: ISING_SIM.py
# Author: JOSEPH M ABRUZZO
# Date: Jan. 2017
# ------------------------
# This program simulates the Ising model of electron spin interaction on a 2D lattice. For further information, see
# <https://en.wikipedia.org/wiki/Ising_model>.


import math
import random
import numpy as np
from graphics import *
import pandas as pd


GRID_DIM = 50
WIN_WIDTH = GRID_DIM * 12
SPIN_FRAC = 0.5
PARAM_J = float(1)
PARAM_BETA = float(100000)


class agent():
    def __init__(self, color, spin, obj):
        self.color = color
        self.spin = spin
        self.obj = obj


def switch(ag):
    if ag.color == "white":
        ag.color = "black"
    else:
        ag.color = "white"
    
    ag.spin = -ag.spin


def prb(h1, h2):
    return math.exp(-PARAM_BETA * float(h1 - h2))


def hamiltonian(vec):
    return -PARAM_J * float(sum(vec))


def initGridVis(grid, win):
    for i in range(GRID_DIM):
        for j in range(GRID_DIM):
            a = grid[i][j]
            
            x1 = j * float(WIN_WIDTH / GRID_DIM)
            y1 = i * float(WIN_WIDTH / GRID_DIM)
            
            p1 = Point(x1, y1)
            p2 = Point(x1 + float(WIN_WIDTH / GRID_DIM), y1 + float(WIN_WIDTH / GRID_DIM))
            
            rect = Rectangle(p1, p2)
            
            rect.setFill(a.color)
            
            rect.draw(win)
            
            a.obj = rect


def simulate(grid, win):
    d1 = random.randint(0, GRID_DIM - 1)
    d2 = random.randint(0, GRID_DIM - 1)
    
    a = grid[d1][d2]
    
    mu = []
    nu = []
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if d1 + j >= 0 and d2 + i >= 0 and d1 + j <= GRID_DIM - 1 and d2 + i <= GRID_DIM - 1:
                if not (i == 0 and j == 0):
                    
                    n = grid[d1 + j][d2 + i]
                    
                    mu.append(a.spin * n.spin)
                    nu.append(a.spin * -n.spin)
    
    if hamiltonian(nu) - hamiltonian(mu) > 0:
        crit = prb(hamiltonian(nu), hamiltonian(mu))
        
        p = random.random()
        
        if crit >= p:
            switch(a)
    
    else:
        switch(a)
    
    r = a.obj
    r.setFill(a.color)


def getAgentAttr():
    s = random.random()
    
    if (s < SPIN_FRAC):
        color = "white"
        spin = -1
    else:
        color = "black"
        spin = 1
    
    obj = None
        
    a = agent(color, spin, obj)
    
    return a


def createAgentGrid():
    g = []
    
    for i in range(GRID_DIM):
        row = []
        
        for j in range(GRID_DIM):
            
            a = getAgentAttr()
            
            row.append(a)
        
        g.append(row)
    
    return g


def main():
    grid = createAgentGrid()
    
    win = GraphWin("ISING", WIN_WIDTH, WIN_WIDTH, autoflush = False)
    
    initGridVis(grid, win)
    
    win.getMouse()
    
    while True:
        simulate(grid, win)
        
        press = win.checkKey()
        if press == "x":
            break

    win.close()


main()