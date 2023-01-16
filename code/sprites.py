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


class Object(Sprite):
	def __init__(self, image, x, y, true_size):
		super().__init__([all_sprites, objects])
		self.image = pygame.transform.scale(image, true_size)
		self.rect = self.image.get_rect().move(x, y)


class Background(Sprite):
	def __init__(self, w, h, x, y):
		super().__init__(btn_bg_group)
		self.image = load_image('bg_button.png')
		self.image = pygame.transform.scale(self.image, (w // 3 - 10, h // 10 - 5))
		self.rect = self.image.get_rect().move(
			x, y)


tile_width = tile_height = 50


class Tile(Sprite):
	def __init__(self, image, pos_x, pos_y):
		super().__init__([tiles, all_sprites])
		self.image = pygame.transform.scale(image, (tile_width, tile_height))
		self.rect = self.image.get_rect().move(
			tile_width * pos_x, tile_height * pos_y)


class CameraGroup(SpriteGroup):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()
	
	def get_surface(self):
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		for sprite in self.sprites():
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)


sprite_group = SpriteGroup()
all_sprites = CameraGroup()
objects = SpriteGroup()
hero_group = CameraGroup()
tiles = SpriteGroup()
btn_bg_group = SpriteGroup()
trees_group = SpriteGroup()
