import sys
import pygame

from funcs import load_image
from start import start_screen
from sprites import hero_group, Player

pygame.init()
screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)
FPS = 50
speed = 1.25

icon = load_image('icon.png')

pygame.display.set_icon(icon)
pygame.display.set_caption("Brave knight")

player = Player(load_image('hero_sheet.png'), 6, 2, 300, 400)
running = True
clock = pygame.time.Clock()

start_screen()


def main_screen():
	global running
	fon = pygame.transform.scale(load_image('lvl1.png'), screen_size)
	screen.blit(fon, (0, 0))
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			player.direction = 'up'
			player.is_moving = True
		elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
			player.direction = 'down'
			player.is_moving = True
		
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			player.direction = 'left'
			player.is_moving = True
			player.flag_le = True
		elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			player.direction = 'right'
			player.is_moving = True
			player.flag_le = False
		
		if player.location == 1:
			fon = pygame.transform.scale(load_image('lvl1.png'), screen_size)
		if player.location == 2:
			fon = pygame.transform.scale(load_image('lvl2.png'), screen_size)
		if player.location == 3:
			fon = pygame.transform.scale(load_image('lvl3.png'), screen_size)
		screen.blit(fon, (0, 0))
		hero_group.draw(screen)
		player.update()
		pygame.display.flip()
		clock.tick(FPS)
	pygame.quit()
	sys.exit()


main_screen()
