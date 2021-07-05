import pygame as pg

class Text:
    def __init__(self, text, size, color, font = None, antialias = True, bg = None):
        self.font = pg.font.Font(font, size)
        self.surface = self.font.render(text, antialias, color, bg)
    
    def blit(self, screen, **pos):
        self.pos = self.surface.get_rect(**pos)
        screen.blit(self.surface, self.pos)


__image_cache = dict()
def load_image(path):
    global __image_cache

    if not path in __image_cache:
        __image_cache[path] = pg.image.load(path)

    return __image_cache[path].copy()

def scale_surface(surface, scale):
    try:
        return pg.transform.smoothscale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))
    except:
        return pg.transform.scale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))

def resize_surface(surface, width: int, height: int):
    try:
        return pg.transform.smoothscale(surface, (width, height))
    except:
        return pg.transform.scale(surface, (width, height))