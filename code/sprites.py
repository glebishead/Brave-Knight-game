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
    def __init__(self, sheet, columns, rows, pos_x, pos_y, start_location=1):
        super().__init__(hero_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows, pos_x, pos_y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.t = pygame.time.get_ticks()
        self.pos = (pos_x, pos_y)
        from main import speed
        self.speed = speed
        self.is_moving = False
        self.direction = None
        self.location = start_location
    
    def cut_sheet(self, sheet, columns, rows, x, y):
        self.rect = pygame.Rect(x, y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (30, 30)))
    
    def update(self):
        if self.is_moving:
            if self.direction is not None:
                self.cur_frame = self.cur_frame + 0.25
            if self.cur_frame > 11:
                self.cur_frame = 1
            if self.cur_frame == 3:
                self.cur_frame += 2
            self.image = self.frames[int(self.cur_frame)]
            if self.direction == 'left':
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            if self.direction == 'left':
                self.image = self.frames[0]
        self.t = pygame.time.get_ticks()

    def move(self):
        x, y = self.pos
        if self.is_moving:
            match self.direction:
                case 'up':
                    y -= self.speed
                case 'down':
                    y += self.speed
                case 'left':
                    x -= self.speed
                case 'right':
                    x += self.speed
        from main import screen_size
        if self.location == 1:
            if x <= 0 and y <= 0:
                self.location = 2
                x, y = screen_size[0] - 30, screen_size[1] - 40
        elif self.location == 2:
            if x <= 0 and 220 <= y <= 300:
                self.location = 3
                x, y = screen_size[0] - 30, screen_size[1] - 220
            if x + 30 > screen_size[0] and y + 40 > screen_size[1]:
                self.location = 1
                x, y = 10, 10
        elif self.location == 3:
            if x + 30 >= screen_size[0] and 220 <= y <= 300:
                self.location = 2
                x, y = 10, screen_size[1] - 220
        if x < 0:
            x = 0
        elif x > screen_size[0] - 30:
            x = screen_size[0] - 30
        if y < 0:
            y = 0
        elif y > screen_size[1] - 40:
            y = screen_size[1] - 40
        self.direction = None
        self.is_moving = False
        self.pos = x, y
        self.rect = self.image.get_rect().move(self.pos)

# class Tree(Sprite):
#     def __init__(self, x, y):
#         super().__init__(trees_group)
#         self.image = pygame.


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
trees_group = SpriteGroup()
