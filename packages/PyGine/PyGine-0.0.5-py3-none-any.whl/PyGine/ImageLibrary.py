import pygame
import sys

class ImageLibrary():
    """ImageLibrary is a class that stores the images loaded by the PyGineGame class, and is used to access them"""
    def __init__(self,assetFolder="Assets"):
        """Constructor for ImageLibrary"""
        self.images = {}
        print()
        assert assetFolder != "", "You must specify an asset folder"
        self.LoadAllImages(sys.path[1]+"/"+assetFolder.removesuffix("/").removeprefix("/"))

    def LoadAllImages(self, path):
        """Load all the images in a folder"""
        import os
        for file in os.listdir(path):
            if file.endswith(".png"):
                self.addImage(file, path +"/"+ file)

    def addImage(self, name, path):
        """Add an image to the library, with a name and a path"""
        self.images[name] = pygame.image.load(path).convert()
        #scale the image to a constant
        self.images[name] = pygame.transform.scale(self.images[name], (100,100))
        self.images[name].set_colorkey((255,255,255))
        self.images[name].convert_alpha()

    def getImage(self, name):
        """Get an image from the library, with a name"""
        if name in self.images:
            return self.images[name]
        else:
            return self.images["default"]

    def removeImage(self, name):
        """Remove an image from the library, with a name"""
        if name in self.images:
            del self.images[name]

    def listImages(self):
        """List all the images in the library"""
        for key in self.images:
            print(key)

    def clear(self):
        """Clear the library"""
        self.images = {}
        self.images["default"] = pygame.image.load("PyGine/DefaultImage.png")
        self.images["default"] = pygame.transform.scale(self.images["default"], (100,100))
        self.images["default"].set_colorkey((255,255,255))
        self.images["default"].convert_alpha()