#!/bin/python
# -*- coding: utf-8 -*-

import sys

LOGLEVEL = 3


def log(message, level=3):
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    if level >= LOGLEVEL:
        print(message, file=sys.stderr)


class Consts(object):
    def __init__(self):
        # Constraints
        self.dummy = 42

        # Constants
        self.DUMMY = 43

        # Configuration
        self.RANDOMNESS = 6

consts = Consts()


class DIR:
    E = 0
    NE = 1
    NW = 2
    W = 3
    SW = 4
    SE = 5
    all = range(6)

E, NE, NW, W, SW, SE = DIR.E, DIR.NE, DIR.NW, DIR.W, DIR.SW, DIR.SE


class GameState(object):
    def __init__(self, consts):
        self.consts = consts
        self.init_entities()

    def init_entities(self):
        pass

    def new_turn(self):
        self.init_entities()


class CommandBuilder(object):
    def wait(self): return "WAIT"


class DecisionMaker(object):
    def __init__(self, state):
        self.state = state

    def decide(self):
        commands = []
        return commands


if __name__ == "__main__":
    state = GameState(consts)
    dm = DecisionMaker(state)

    # game loop
    while True:
        # process input, update state

        decisions = dm.decide()
        for cmd in decisions:
            print(cmd)
