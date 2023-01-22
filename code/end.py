import sys
import pygame


from funcs import load_image

screen_size = width, height = (1280, 800)


def end_screen():
    running = True
    screen = pygame.display.set_mode(screen_size)
    fon = pygame.transform.scale(load_image('images\\end_bg.jpg'), screen_size)
    screen.blit(fon, (0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw(screen)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


def draw(screen):
    width, height = screen.get_size()
    font = pygame.font.Font(None, 40)
    texts = ["Благодарим от всей души", "За прохождение игры", "Brave Knight", "Желаем Вам хорошего дня)"]
    for i in range(len(texts)):
        pygame.draw.rect(screen, (180, 180, 180), [
            width // 3 * 2, 10 + i * height // 10,
            width // 3 - 10, height // 10 - 5], 5)
        screen.blit(font.render(texts[i], True, (200, 200, 200)),
                    (width // 3 * 2 + 10, (i + 1) * height // 10 - height // 20 - 10))