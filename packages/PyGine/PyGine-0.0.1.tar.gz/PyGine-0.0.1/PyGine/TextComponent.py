from PyGine.Camera import Camera
from PyGine.Component import Component
import PyGine.PyGineGame as Game
import pygame as pg


from PyGine.Transform import Transform


class TextComponent(Component) :
    def __init__(self, parent,text = " ",color = (255,0,255)):
        super().__init__(parent)
        self.transform = Transform()
        self.text = text
        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.color = color
        self.textcmp =self.font.render(self.text,True,self.color)

    def start(self):
        pass

    def setText(self,text):
        self.textcmp = self.font.render(text,True,self.color)

    def update(self,dt):
        Game.get().surface.blit(self.textcmp,((int(self.transform.position.x + self.parent.transform.position.x - Camera.DX ),int(self.transform.position.y + self.parent.transform.position.y- Camera.DY) ), (int(self.transform.scale.x*Camera.ZX), int(self.transform.scale.y*Camera.ZY))))

