import sys
import pygame
import os

from funcs import load_image, load_level
from sprites import all_sprites, Decoration, Tile
from Player import Player
from start import start_screen


class Game:
	def __init__(self):
		pygame.init()
		self.screen_size = (800, 500)
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
		for i in range(2):
			self.tree = Decoration(load_image('tree.png'), i * 70, i * 120)
		self.generate_level()
	
	def generate_level(self):
		level = load_level('map.map')
		for y in range(len(level)):
			for x in range(len(level[y])):
				if level[y][x] == '.':
					pass
				elif level[y][x] == '#':
					Tile(load_image('wall2.png'), x, y)
		
	def run(self):
		self.fon = pygame.transform.scale(load_image('fon.png'), self.screen_size)
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
			
			all_sprites.get_surface()
			self.screen.blit(self.fon, (0, 0))
			all_sprites.custom_draw(self.player)
			self.player.input_keys(pygame.key.get_pressed())
			self.player.update()
			pygame.display.update()
			self.clock.tick(self.FPS)
		pygame.quit()
		sys.exit()


if __name__ == '__main__':
	game = Game()
	game.run()