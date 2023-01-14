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
		super().__init__(all_sprites)
		self.frames = []
		self.cut_sheet(sheet, columns, rows, pos_x, pos_y)
		self.cur_frame = 0
		self.image = self.frames[self.cur_frame]
		self.t = pygame.time.get_ticks()
		self.pos = (pos_x, pos_y)
		self.speed = 4
		self.is_moving = False
		self.direction = None
		self.flag_le = False
		self.location = start_location
	
	def cut_sheet(self, sheet, columns, rows, x, y):
		self.rect = pygame.Rect(-10, -100, sheet.get_width() // columns,
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
				self.cur_frame = 3
			if self.cur_frame == 3:
				self.cur_frame += 2
			self.image = self.frames[int(self.cur_frame)]
			if self.flag_le:
				self.image = pygame.transform.flip(self.image, True, False)
		else:
			self.image = self.frames[0]
			if self.flag_le:
				self.image = pygame.transform.flip(self.image, True, False)
		self.t = pygame.time.get_ticks()
		self.move()
	
	def input_keys(self, keys):
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			self.direction = 'up'
			self.is_moving = True
		elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self.direction = 'down'
			self.is_moving = True
		
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.direction = 'left'
			self.is_moving = True
			self.flag_le = True
		elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.direction = 'right'
			self.is_moving = True
			self.flag_le = False
	
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
		self.is_moving = False
		self.pos = x, y
		self.rect = self.image.get_rect().move(self.pos)


class Tree(Sprite):
	def __init__(self, x, y):
		super().__init__(all_sprites)
		self.image = load_image('tree.png')
		self.rect = self.image.get_rect().move(x, y)


class Background(Sprite):
	def __init__(self, w, h, x, y):
		super().__init__(btn_bg_group)
		self.image = load_image('bg_button.png')
		self.image = pygame.transform.scale(self.image, (w // 3 - 10, h // 10 - 5))
		self.rect = self.image.get_rect().move(
			x, y)


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
btn_bg_group = SpriteGroup()
trees_group = SpriteGroup()
