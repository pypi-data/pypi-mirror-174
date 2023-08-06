import pygame as pg

class KeyListener :
    stroke = 0


def getPressed(key):
    return pg.key.get_pressed()[key]

