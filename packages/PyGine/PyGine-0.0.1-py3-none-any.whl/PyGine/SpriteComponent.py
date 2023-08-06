import PyGine.PyGineGame as Window
import pygame as pg
import pygame.gfxdraw as gfxdraw
from PyGine.Component import Component


class SpriteComponent(Component) :
    def __init__(self,parent, sprite=" ") :
        super().__init__(parent)
        self.sprite = sprite
        self.parent = parent

    def start(self):
        pass

    def update(self,dt) :
        pass

    def getSprite(self) :
        return self.sprite

    def setSprite(self, sprite) :
        self.sprite = sprite