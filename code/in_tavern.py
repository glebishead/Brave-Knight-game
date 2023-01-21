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
				Tile(load_image('wood_boards.png'), tile_width * x - 1000, tile_height * y, tavern_group)
				seller = Object(pygame.transform.flip(load_image('seller.png'), True, False),
				       x * tile_width - 1000, y * tile_height, (40, 60), tavern_group)
	player.pos = (-800, 410)
	tavern_group.get_surface()
	hero_group.get_surface()
	
	texts = ["Здравствуй, дорогой рыцарь!", "Помоги мне, импы мешают поставкам"]
	text_id = 0
	font = pygame.font.Font(None, 40)
	flag_moving = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.K_q:
				player.location = 1
				return
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if text_id == 0:
					if 400 <= event.pos[0] <= 1000 and 600 <= event.pos[1] <= 780:
						texts = ["Убей импов в лесу", "и я тебя вознагражу!"]
						text_id = 1
				elif text_id == 1:
					if 400 <= event.pos[0] <= 1000 and 600 <= event.pos[1] <= 780:
						texts = ["Без пива нет жизни...", "А теперь иди."]
						text_id = 2
				elif text_id == 2:
					if 400 <= event.pos[0] <= 1000 and 600 <= event.pos[1] <= 780:
						return
				
		screen.fill((0, 0, 0))
		if flag_moving:
			player.input_keys(pygame.key.get_pressed())
		player.update()
		tavern_group.custom_draw(player)
		hero_group.custom_draw(player)
		
		if player.rect.colliderect(seller.rect):
			flag_moving = False
			pygame.draw.rect(screen, (40, 40, 40), (400, 600, 600, 180))
			pygame.draw.rect(screen, (255, 255, 255), (400, 600, 600, 180), 10)
			for i in range(len(texts)):
				text = font.render(texts[i], True, (255, 255, 255))
				screen.blit(text, (420, 620 + i * 40))
		pygame.display.flip()
		clock.tick(FPS)
	pygame.quit()
	sys.exit()