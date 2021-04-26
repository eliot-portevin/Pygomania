import pygame
import json

class Spritesheet:
    def __init__(self,filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.metadata = self.filename.replace('png','json')
        try:
            with open(self.metadata) as f:
                self.data = json.load(f)
            f.close()
        except :
            pass
    def get_sprites(self,x,y,w,h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0,0),(x,y,w,h))
        return sprite

    def parse_sprites(self,name):
        sprite = self.data['frames'][name]['frame']
        x,y,w,h = sprite['x'],sprite['y'],sprite['w'],sprite['h']
        image = self.get_sprites(x,y,w,h)
        return image
