import sys
import pygame
import os

from funcs import load_image, load_level
from sprites import all_sprites, Object, Tile, hero_group, Enemy, enemy_group
from Player import Player
from start import start_screen


class Game:
	def __init__(self):
		pygame.init()
		self.screen_size = (1280, 800)
		self.screen = pygame.display.set_mode(self.screen_size)
		pygame.mixer.music.load('../data/bg_music.wav')
		pygame.mixer.music.play(-1)
		pygame.mixer.music.set_volume(0.2)
		
		self.FPS = 50
		self.speed = 4
		self.quest_started = True
		
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
		self.player = Player(all_sprites, load_image('hero_sheet.png'), 6, 2, 300, 400)
		self.generate_level1()
	
	def generate_level1(self):
		level = load_level('map.map')
		from sprites import tile_width, tile_height
		for y in range(len(level)):
			for x in range(len(level[y])):
				if level[y][x] == '.':
					Tile(load_image('road.png'), tile_width * x, tile_height * y, all_sprites)
				elif level[y][x] == '#':
					Object(load_image('wall2.png'), x * tile_width, y * tile_height, (60, 60), all_sprites)
		decorations = load_level('decorations_map.map')
		for y in range(len(decorations)):
			for x in range(len(decorations[y])):
				if decorations[y][x] == '.':
					Tile(load_image('grass.png'), tile_width * x, tile_height * y, all_sprites)
				elif decorations[y][x] == '@':
					Object(load_image('home1.png'), x * tile_width, y * tile_height, (120, 200), all_sprites)
				elif decorations[y][x] == '$':
					Object(load_image('tavern.png'), x * tile_width, y * tile_height, (120, 200), all_sprites)
				elif decorations[y][x] == '!':
					Tile(load_image('grass.png'), tile_width * x, tile_height * y, all_sprites)
					Object(load_image('tree.png'), x * tile_width, y * tile_height,
					       (tile_width, tile_height), all_sprites)
	
	def generate_level3(self):
		level = load_level('map3.map')
		from sprites import tile_width, tile_height
		for y in range(len(level)):
			for x in range(len(level[y])):
				if level[y][x] == '!':
					Object(load_image('tree.png'), x * tile_width + 3800, y * tile_height,
					       (tile_width, 20 + tile_height), all_sprites)
				elif level[y][x] == '@':
					Enemy(load_image('demon_ic.png'), x * tile_width + 3800, y * tile_height,
					       (tile_width, tile_height), all_sprites)
		
	def run(self):
		self.fon = pygame.transform.scale(load_image('fon.png'), self.screen_size)
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
			self.screen.blit(self.fon, (0, 0))
			
			if self.player.location == 1:
				all_sprites.get_surface()
				hero_group.get_surface()
				all_sprites.custom_draw(self.player)
				self.player.input_keys(pygame.key.get_pressed())
				self.player.update()
				for el in enemy_group:
					el.fight(self.player)
				
			elif self.player.location == 2:
				from in_tavern import tavern_screen
				pos = self.player.pos
				tavern_screen(self.player, self.clock, self.FPS)
				self.player.pos = pos
				self.quest_started = True
				self.player.location = 1
				
			if self.player.pos[0] >= 3000 and self.quest_started:
				pygame.mixer.music.load('../data/Tooth-and-Claw.wav')
				pygame.mixer.music.play(-1)
				pygame.mixer.music.set_volume(0.2)
				self.fon = pygame.transform.scale(load_image('dark_fon.png'), self.screen_size)
				self.generate_level3()
				self.quest_started = False
				
			self.clock.tick(self.FPS)
			hero_group.custom_draw(self.player)
			pygame.display.flip()
		pygame.quit()
		sys.exit()


if __name__ == '__main__':
	game = Game()
	game.run()