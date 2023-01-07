import sys
import pygame

from funcs import load_image
from start import start_screen
from sprites import hero_group, sprite_group


pygame.init()
screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)
FPS = 50

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


icon = load_image('icon.png')

pygame.display.set_icon(icon)
pygame.display.set_caption("Brave knight")

player = None
running = True
clock = pygame.time.Clock()


start_screen()


def main_screen():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_UP]:
        #     move(hero, "up")
        # elif keys[pygame.K_DOWN]:
        #     move(hero, "down")
        # elif keys[pygame.K_LEFT]:
        #     move(hero, "left")
        # elif keys[pygame.K_RIGHT]:
        #     move(hero, "right")
        screen.fill(pygame.Color("black"))
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


main_screen()
