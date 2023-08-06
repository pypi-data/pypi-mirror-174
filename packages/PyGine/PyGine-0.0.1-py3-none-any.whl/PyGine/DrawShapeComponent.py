import PyGine.PyGineGame as Game
import pygame as pg

from PyGine.Camera import Camera
from PyGine.Component import Component
from PyGine.Transform import Transform


class DrawShapeComponent(Component) :
    def __init__(self,parent,color , shape="rect"):
        super().__init__(parent)
        self.shape = shape
        self.parent = parent
        self.transform = parent.transform
        self.color = color

    def start(self):
        pass

    def update(self,dt):
        if self.shape == "rect" :
            pg.draw.rect(Game.get().surface, self.color,((
                                                     int(self.transform.position.x - Camera.DX),
                                                     int(self.transform.position.y - Camera.DY) ),
                                                     (int(self.transform.scale.x * Camera.ZX),
                                                      int(self.transform.scale.y * Camera.ZY))))
        elif self.shape == "circle" :
            pg.draw.circle(Game.get().surface,self.color,(int(self.transform.position.x - Camera.DX),
                                                     int(self.transform.position.y - Camera.DY) ) , self.transform.scale.x*Camera.ZX)
    def getSprite(self):
        return self.sprite
    def setSprite(self, sprite):
        self.sprite = sprite

