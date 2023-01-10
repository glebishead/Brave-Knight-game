import sys
import pygame

from funcs import load_image
from start import start_screen
from sprites import hero_group, Player


pygame.init()
screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)
FPS = 50

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

icon = load_image('icon.png')

pygame.display.set_icon(icon)
pygame.display.set_caption("Brave knight")

player = Player(300, 400)
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
        if keys[pygame.K_UP]:
            player.speed_y -= 2
        if keys[pygame.K_DOWN]:
            player.speed_y += 2
        if keys[pygame.K_LEFT]:
            player.speed_x -= 2
        if keys[pygame.K_RIGHT]:
            player.speed_x += 2
        if keys[pygame.K_w]:
            player.speed_y -= 2
        if keys[pygame.K_s]:
            player.speed_y += 2
        if keys[pygame.K_a]:
            player.speed_x -= 2
        if keys[pygame.K_d]:
            player.speed_x += 2
        player.move()
        screen.blit(fon, (0, 0))
        hero_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


main_screen()
