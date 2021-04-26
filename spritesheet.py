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
    def get_sprites(self,x,y,w,h,x_o,y_o,w_o,h_o):
        sprite = pygame.Surface((w_o,h_o))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(x_o,y_o),(x,y,w,h))
        return sprite

    def parse_sprites(self,name):
        sprite = self.data['frames'][name]
        in_image = sprite['frame']
        original = sprite['spriteSourceSize']
        size = sprite['sourceSize']
        x,y,w,h = in_image['x'],in_image['y'],in_image['w'],in_image['h']
        x_o,y_o,w_o,h_o = original['x'],original['y'],size['w'],size['h']
        image = self.get_sprites(x,y,w,h,x_o,y_o,w_o,h_o)
        return image