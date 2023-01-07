import pygame

from funcs import load_image


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        from main import tile_width, tile_height, player_image
        super().__init__(hero_group)
        self.image = pygame.transform.scale(player_image, (tile_width, tile_height))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        from main import tile_width, tile_height
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


class Background(Sprite):
    def __init__(self, w, h, x, y):
        super().__init__(btn_bg_group)
        self.image = load_image('bg_button.png')
        self.image = pygame.transform.scale(self.image, (w // 3 - 10, h // 10 - 5))
        self.rect = self.image.get_rect().move(
            x, y)


sprite_group = SpriteGroup()
hero_group = SpriteGroup()
btn_bg_group = SpriteGroup()
