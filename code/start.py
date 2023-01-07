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
    from main import btn_bg_group, Background
    width, height = screen.get_size()
    font = pygame.font.Font(None, 50)
    texts = ["New game", "Continue", "Load"]
    for i in range(3):
        bg = Background(width, height, width // 3 * 2, 10 + i * height // 10)
    btn_bg_group.draw(screen)
    for i in range(3):
        pygame.draw.rect(screen, (120, 55, 0), [
            width // 3 * 2, 10 + i * height // 10,
            width // 3 - 10, height // 10 - 5], 5)
        screen.blit(font.render(texts[i], True, (190, 255, 190)),
                    (width // 3 * 2 + 10, (i + 1) * height // 10 - height // 20 - 10))
