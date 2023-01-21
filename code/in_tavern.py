import sys
import pygame

from funcs import load_level, load_image
from sprites import Tile, Object, tile_width, tile_height, tavern_group, hero_group

screen_size = width, height = (1280, 800)


def tavern_screen(player, clock, FPS):
	running = True
	screen = pygame.display.set_mode(screen_size)
	screen.fill((0, 0, 0))
	tavern = load_level('tavern.map')
	for y in range(len(tavern)):
		for x in range(len(tavern[y])):
			if tavern[y][x] == '.':
				Tile(load_image('wood_boards.png'), tile_width * x - 1000, tile_height * y, tavern_group)
			elif tavern[y][x] == '#':
				Object(load_image('wall2.png'), x * tile_width - 1000, y * tile_height, (60, 60), tavern_group)
			elif tavern[y][x] == '@':
				Object(pygame.transform.flip(load_image('seller.png'), True, False),
				       x * tile_width - 1000, y * tile_height, (40, 60), tavern_group)
	player.pos = (-800, 410)
	tavern_group.get_surface()
	hero_group.get_surface()
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				player.location = 1
				return
		player.input_keys(pygame.key.get_pressed())
		player.update()
		screen.fill((0, 0, 0))
		tavern_group.custom_draw(player)
		# all_sprites.custom_draw(player)
		hero_group.custom_draw(player)
		pygame.display.flip()
		clock.tick(FPS)
	pygame.quit()
	sys.exit()