from PyGine.Component import Component
import pygame as pg
import PyGine.PyGinegame as Game
from PyGine.Camera import Camera
class SpriteComponent(Component) :
    def __init__(self,parent, sprite=" ") :
        super().__init__(parent)
        self.sprite = sprite
        self.parent = parent

    def start(self):
        pass

    def update(self,dt) :
        #scale the img to the transform scale
        img = pg.transform.scale(Game.get().imageLib.getImage(self.sprite), (int(self.parent.transform.scale.x*Camera.ZX), int(self.parent.transform.scale.y*Camera.ZY)))
        Game.get().surface.blit(img,((int(self.parent.transform.position.x - Camera.DX ),int(self.parent.transform.position.y- Camera.DY) )))

    def getSprite(self) :
        return self.sprite

    def setSprite(self, sprite) :
        self.sprite = sprite