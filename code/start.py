import sys
import pygame


from funcs import load_image


def start_screen():
    from main import screen_size, clock, FPS, running

    width, height = screen_size
    screen = pygame.display.set_mode(screen_size)
    fon = pygame.transform.scale(load_image('start_background.png'), screen_size)
    screen.blit(fon, (0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if width // 3 * 2 <= event.pos[0] <= width - 10 and 10 <= event.pos[1] <= height // 10:
                    return
        draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()


def draw(screen):
    width, height = screen.get_size()
    pygame.draw.rect(screen, (180, 20, 20), [width // 3 * 2, 10, width // 3 - 10, height // 10])
    font = pygame.font.Font(None, 30)
    text = font.render("New game", True, (10, 25, 10))
    screen.blit(text, (width // 3 * 2 + 10, height // 10 - height // 20))
