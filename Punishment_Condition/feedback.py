import pygame as pg
import pandas as pd

df = pd.DataFrame(columns=['Bin', 'Start', 'End', 'Difference'])

class Indecision(pg.sprite.Sprite):
    """Indecision feedback"""

    defaultlife = 25
    end = 0
    images = []
    startAgain = False

    def __init__(self, pos):
        self.start = pg.time.get_ticks()
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)
        self.defaultlife = len(self.images)
        self.life = -1
    
    def update(self):
        self.life = self.life + 1
        self.image = self.images[self.life]
        if (pg.time.get_ticks()-self.start) >= 1895:
            print("Tiempo estimulo ", pg.time.get_ticks() - self.start)
            self.kill()
            df.loc[-1 ] = ["Ind", self.start, pg.time.get_ticks(), pg.time.get_ticks()-self.start]
            df.index =  df.index + 1
            df.to_excel("feedbackTimes_av.xlsx")
        elif self.life >= self.defaultlife-1:
            self.life = 0
