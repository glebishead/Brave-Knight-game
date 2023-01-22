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
	def __init__(self, image, x, y, true_size, *groups):
		super().__init__([*groups, objects])
		self.image = pygame.transform.scale(image, true_size)
		self.rect = self.image.get_rect().move(x, y)


class Enemy(Object):
	def __init__(self, image, x, y, true_size, group):
		super().__init__(image, x, y, true_size, group, enemy_group)
	
	def fight(self, player):
		if self.rect.colliderect(player.rect):
			from fight import main
			if player.imp_killed < 5:
				if not main('imp_red'):
					self.kill()
					player.imp_killed += 1
				else:
					player.pos = player.pos[0] - player.speed, player.pos[1] + player.speed
					player.rect = player.image.get_rect().move(player.pos)
			else:
				pygame.mixer.music.load('../data/Death-or-Sovngard.wav')
				pygame.mixer.music.play(-1)
				pygame.mixer.music.set_volume(0.2)
				if not main('demon_axe_red'):
					from end import end_screen
					end_screen()
				else:
					player.pos = player.pos[0] - player.speed, player.pos[1] + player.speed
					player.rect = player.image.get_rect().move(player.pos)
				

class Background(Sprite):
	def __init__(self, w, h, x, y):
		super().__init__(btn_bg_group)
		self.image = load_image('bg_button.png')
		self.image = pygame.transform.scale(self.image, (w // 3 - 10, h // 10 - 5))
		self.rect = self.image.get_rect().move(
			x, y)


tile_width = tile_height = 50


class Tile(Sprite):
	def __init__(self, image, pos_x, pos_y, group):
		super().__init__([tiles, group])
		self.image = pygame.transform.scale(image, (tile_width, tile_height))
		self.rect = self.image.get_rect().move(
			pos_x, pos_y)


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

tavern_group = CameraGroup()
enemy_group = SpriteGroup()

objects = SpriteGroup()
hero_group = CameraGroup()
tiles = SpriteGroup()
btn_bg_group = SpriteGroup()
