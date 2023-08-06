
import pygame as pg

from PyGine.Camera import Camera
from PyGine.Component import Component
import PyGine.PyGineGame as Game
from PyGine.Transform import Transform


class BoxColliderComponent(Component) :
    def __init__(self,parent) :
        super().__init__(parent)
        self.parent = parent
        self.transform = parent.transform

    def update(self,dt) :
        pg.draw.rect(Game.get().surface, (0,0,0),((
                                                 int(self.transform.position.x - Camera.DX),
                                                 int(self.transform.position.y - Camera.DY) ),
                                                 (int(self.transform.scale.x * Camera.ZX),
                                                  int(self.transform.scale.y * Camera.ZY))),1)


    def collide(self,o):

        if (o.transform.position.x+o.transform.scale.x > self.transform.position.x > o.transform.position.x ) or \
                (self.transform.position.x+self.transform.scale.x > o.transform.position.x > self.transform.position.x ):
            if (o.transform.position.y + o.transform.scale.y > self.transform.position.y > o.transform.position.y) or \
                    (self.transform.position.y + self.transform.scale.y > o.transform.position.y > self.transform.position.y):
                return True
        return False
