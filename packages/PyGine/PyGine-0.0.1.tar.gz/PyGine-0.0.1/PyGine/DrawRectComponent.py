import PyGine.PyGineGame as Game
import pygame as pg

from PyGine.Camera import Camera
from PyGine.Component import Component
from PyGine.Transform import Transform


class DrawRectComponent(Component) :
    def __init__(self,parent,color ) :
        super().__init__(parent)

        self.parent = parent

        self.transform = parent.transform
        self.color = color

    def start(self):
        pass

    def update(self,dt) :
        pg.draw.rect(Game.get().surface, self.color,((
                                                 int(self.transform.position.x - Camera.DX),
                                                 int(self.transform.position.y - Camera.DY) ),
                                                 (int(self.transform.scale.x * Camera.ZX),
                                                  int(self.transform.scale.y * Camera.ZY))))

    def getSprite(self) :
        return self.sprite

    def setSprite(self, sprite) :
        self.sprite = sprite