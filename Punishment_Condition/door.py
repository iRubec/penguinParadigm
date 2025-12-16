import pygame as pg

SCREENRECT = pg.Rect(0, 0, 1280, 960)

class LeftDoor(pg.sprite.Sprite):
    """
        Create a door
        Arguments:
         pos = (x, y): left, top position of the door
    """
    
    play = False
    selected = False
    scale = 0.2
    baseImage = pg.image
    passImages = []
    disappear_iter = 0
    disappear = False

    init_pos = (SCREENRECT.w/2, SCREENRECT.h/2+20)

    def __init__(self, screenSize):
        self.init_pos = (screenSize[0]/2, screenSize[1]/2+20)

        pg.sprite.Sprite.__init__(self)
        self.pos = self.init_pos
        self.image = self.baseImage

        self.rect = self.image.get_rect(midright = self.init_pos)

       
    def doorCollided(self):
        self.disappear = True
    
    def update(self):
        if self.play:
            self.scale += 0.005
            if not self.disappear:
                self.image = pg.transform.scale_by(self.baseImage, self.scale)
            else:
                self.image = pg.transform.scale_by(self.passImages[self.disappear_iter], self.scale)
                self.disappear_iter += 1
                if self.disappear_iter >= 13:
                    self.disappear_iter = 13

            if self.pos[1] >= self.init_pos[1]+175:
                self.pos = (self.pos[0], self.pos[1]+10)
            else:
                self.pos = (self.pos[0]-0.1, self.pos[1]+1.05)
            self.rect = self.image.get_rect(midright = self.pos)

            
            if self.pos[1] >= SCREENRECT.height  + self.rect.height/2:
                    self.scale = 0.2
                    self.pos = self.init_pos
                    self.image = self.baseImage
                    self.disappear_iter = 0
                    self.disappear = False
                    self.play = False

class RightDoor(pg.sprite.Sprite):
    """
        Create a door
        Arguments:
         pos = (x, y): left, top position of the door
    """
    
    play = False
    selected = False
    scale = 0.2
    baseImage = pg.image
    passImages = []
    disappear_iter = 0
    disappear = False

    init_pos = (SCREENRECT.w/2, SCREENRECT.h/2+20)

    def __init__(self, screenSize):
        self.init_pos = (screenSize[0]/2, screenSize[1]/2+20)

        pg.sprite.Sprite.__init__(self)
        self.pos = self.init_pos
        self.image = self.baseImage

        self.rect = self.image.get_rect(midleft = self.init_pos)
       
    def doorCollided(self):
        self.disappear = True
    
    def update(self):
        if self.play:
            self.scale += 0.005
            if not self.disappear:
                self.image = pg.transform.scale_by(self.baseImage, self.scale)
            else:
                self.image = pg.transform.scale_by(self.passImages[self.disappear_iter], self.scale)
                self.disappear_iter += 1
                if self.disappear_iter >= 13:
                    self.disappear_iter = 13

            if self.pos[1] >= self.init_pos[1]+175:
                self.pos = (self.pos[0], self.pos[1]+10)
            else:
                self.pos = (self.pos[0]+0.1, self.pos[1]+1.05)
            self.rect = self.image.get_rect(midleft = self.pos)
            
            if self.pos[1] >= SCREENRECT.height  + self.rect.height/2:
                    self.scale = 0.2
                    self.pos = self.init_pos
                    self.image = self.baseImage
                    self.disappear_iter = 0
                    self.disappear = False
                    self.play = False

class DoorCenter(pg.sprite.Sprite):
    """
        Create the door center part
    """
    play = False
    scale = 0.2
    disappear_iter = 0
    baseImage = pg.image
    images = []

    init_pos = (SCREENRECT.w/2, SCREENRECT.h/2+20)

    def __init__(self, screenSize):
        self.init_pos = (screenSize[0]/2, screenSize[1]/2+20)
        pg.sprite.Sprite.__init__(self)
        self.pos = self.init_pos
        self.image = self.baseImage
        self.rect = self.image.get_rect(center= self.init_pos)
    
    def getHeight(self):
        return self.pos[1]
    
    def update(self):
        if self.play:
            self.scale += 0.005
            self.image = pg.transform.scale_by(self.baseImage, self.scale)

            if self.pos[1] >= self.init_pos[1]+175:
                #self.disappear = True
                self.pos = (self.pos[0], self.pos[1]+10)
            else:
                self.pos = (self.pos[0], self.pos[1]+1.05)
            self.rect = self.image.get_rect(center = self.pos)

            if self.pos[1] >= SCREENRECT.height + self.rect.height/2:
                self.scale = 0.2
                self.pos = self.init_pos
                self.image = self.baseImage
                self.play = False