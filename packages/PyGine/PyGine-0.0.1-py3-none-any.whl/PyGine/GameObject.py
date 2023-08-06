from abc import ABC

from PyGine import PyGineGame
from PyGine.Camera import Camera
from PyGine.Transform import Transform


class GameObject(ABC) :
    def __init__(self,name="",tags=["gameObjects"]):
        self.tags = tags
        self.name = name
        self.transform = Transform()
        self.Components = []
        self.destroy = False
        self.tracked = False
        self.Used = False
        self.started = False

    def start(self):
        pass

    def earlyStart(self):
        pass


    def Mstart(self):
        if not self.started :
            self.earlyStart()
            for c in self.Components :
                c.Mstart()
            self.started = True
            self.Used = True

            self.start()

    def update(self,dt):
        pass

    def Mupdate(self,dt):


        if(not self.destroy) :
            for composant in self.Components:
                composant.update(dt)
                if(self.destroy) :
                    break
        else :
            PyGineGame.get().CurrentScene.removeGameObject(self)

        if self.tracked :
            Camera.DX = self.transform.position.x - PyGineGame.get().width/2
            Camera.DY = self.transform.position.y - PyGineGame.get().height/2

        self.update(dt)

    def addComponent(self, composant):
        if self.Used :
            composant.start()
        self.Components.append(composant)



    def AttachCamera(self,state):
        self.tracked = state


    def getComponent(self,class_) :
        for el in self.Components :
            if el.__class__ == class_ :
                return el
        return None

    def Mend(self):
        self.end()

    def end(self):
        pass