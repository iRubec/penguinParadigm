import pygame as pg
import pandas as pd

df = pd.DataFrame(columns=['Bin', 'Start', 'End', 'Difference'])

class Correct(pg.sprite.Sprite):
    """Correct feedback"""

    defaultlife = 8
    images = []
    end = 0

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=(pos[0], pos[1]-30))
        self.defaultlife = len(self.images)
        self.life = -1
        self.start = pg.time.get_ticks()
        pg.mixer.Sound("res/audios/correct.wav").play()

    def update(self):
        self.life = self.life + 1
        self.image = self.images[self.life]
        end = pg.time.get_ticks()
        if (end-self.start) >= 1895:
            #print("Tiempo estimulo ", pg.time.get_ticks() - self.start)
            self.kill()
            
            df.loc[-1 ] = ["Correct", self.start, end, end-self.start]
            df.index =  df.index + 1
            df.to_excel("feedbackTimes.xlsx")
            
        elif self.life >= self.defaultlife-1:
            self.life = 0

class Indecision(pg.sprite.Sprite):
    """Indecision feedback"""

    defaultlife = 25
    end = 0
    images = []
    startAgain = False

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)
        self.defaultlife = len(self.images)
        self.life = -1
        self.start = pg.time.get_ticks()
    
    def update(self):
        self.life = self.life + 1
        self.image = self.images[self.life]
        end = pg.time.get_ticks()
        if (end-self.start) >= 1895:
            #print("Tiempo estimulo ", pg.time.get_ticks() - self.start)
            self.kill()
            
            df.loc[-1 ] = ["Ind", self.start, end, end-self.start]
            df.index =  df.index + 1
            df.to_excel("feedbackTimes.xlsx")
        elif self.life >= self.defaultlife-1:
            self.life = 0