import sys
import pygame
import os

from funcs import load_image, load_level
from sprites import all_sprites, Object, Tile, hero_group
from Player import Player
from start import start_screen


class Game:
	def __init__(self):
		pygame.init()
		self.screen_size = (1280, 800)
		self.screen = pygame.display.set_mode(self.screen_size)
		
		self.FPS = 50
		# speed = 1.5
		self.speed = 4
		
		self.init_ui()
		self.init_game()

		self.running = True
		self.clock = pygame.time.Clock()

		start_screen()
	
	def init_ui(self):
		icon = load_image('icon.png')
		pygame.display.set_icon(icon)
		
		pygame.display.set_caption("Brave knight")
	
	def init_game(self):
		self.player = Player(load_image('hero_sheet.png'), 6, 2, 300, 400)
		self.generate_level()
	
	def generate_level(self):
		level = load_level('map.map')
		from sprites import tile_width, tile_height
		for y in range(len(level)):
			for x in range(len(level[y])):
				if level[y][x] == '.':
					Tile(load_image('road.png'), x, y)
				elif level[y][x] == '#':
					Object(load_image('wall2.png'), x * tile_width, y * tile_height, (60, 60))
		decorations = load_level('decorations_map.map')
		for y in range(len(decorations)):
			for x in range(len(decorations[y])):
				if decorations[y][x] == '.':
					Tile(load_image('grass.png'), x, y)
				elif decorations[y][x] == '@':
					Object(load_image('home1.png'), x * tile_width, y * tile_height, (120, 200))
				elif decorations[y][x] == '!':
					Tile(load_image('grass.png'), x, y)
					Object(load_image('tree.png'), x * tile_width, y * tile_height, (tile_width, tile_height))
		
	def run(self):
		self.fon = pygame.transform.scale(load_image('fon.png'), self.screen_size)
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
			
			all_sprites.get_surface()
			hero_group.get_surface()
			self.screen.blit(self.fon, (0, 0))
			all_sprites.custom_draw(self.player)
			self.player.input_keys(pygame.key.get_pressed())
			self.player.update()
			self.clock.tick(self.FPS)
			hero_group.custom_draw(self.player)
			pygame.display.flip()
		pygame.quit()
		sys.exit()


if __name__ == '__main__':
	game = Game()
	game.run()