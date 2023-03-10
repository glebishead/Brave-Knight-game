import sys
import pygame


from funcs import load_image

screen_size = width, height = (1280, 800)


def start_screen():
    running = True
    screen = pygame.display.set_mode(screen_size)
    fon = pygame.transform.scale(load_image('images\\start_background.png'), screen_size)
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
    pygame.quit()
    sys.exit()


def draw(screen):
    from sprites import btn_bg_group, Background
    width, height = screen_size
    font = pygame.font.Font(None, 50)
    texts = ["New game"]
    for i in range(len(texts)):
        bg = Background(width, height, width // 3 * 2, 10 + i * height // 10)
    btn_bg_group.draw(screen)
    for i in range(len(texts)):
        pygame.draw.rect(screen, (120, 55, 0), [
            width // 3 * 2, 10 + i * height // 10,
            width // 3 - 10, height // 10 - 5], 5)
        screen.blit(font.render(texts[i], True, (190, 255, 190)),
                    (width // 3 * 2 + 10, (i + 1) * height // 10 - height // 20 - 10))
