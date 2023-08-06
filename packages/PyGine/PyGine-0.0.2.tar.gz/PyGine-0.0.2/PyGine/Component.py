from abc import ABC


class Component(ABC) :
    def __init__(self, parent,name="") :
        self.name = name
        self.parent = parent


    def Mstart(self):
        self.earlyStart()
        self.start()

    def start(self):
        pass

    def earlyStart(self):
        pass

    def update(self,dt):
        pass