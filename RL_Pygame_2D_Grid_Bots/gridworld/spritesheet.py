import pygame
import numpy as np

class spritesheet(object):

    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

def make_sprite_array(ss, fr, w, h):
    ness = []
    for i in np.arange(fr):
        ness.append(ss.image_at((i*w, 0, w, h), (255, 255, 255)))

    return ness