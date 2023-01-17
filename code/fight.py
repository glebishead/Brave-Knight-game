import pygame
import os
import sys
from random import randint
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.progressbar import ProgressBar
from funcs import load_image


pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 12
quit = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.max_hp = 50
        self.cur_hp = 50
        self.min_damage = 11
        self.max_damage = 14
        self.money = 50

        self.images = []
        self.index = 0

        hp_bar = ProgressBar(screen, 200, 100, 300, 40, lambda: self.cur_hp / self.max_hp, completedColour=(255, 0, 0))

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.images = []
            for i in range(3):
                for _ in range(2):
                    self.images.append(pygame.transform.scale(load_image(
                        f"..\data\pack_loreon_char_free\sword_1\idle_{i}.png"), (500, 350)))
            self.index = 0
            self.rect = pygame.Rect(100, 100, 100, 100)
        self.image = self.images[self.index]

    def attack(self, menu, enemy):
        dmg = randint(self.min_damage, self.max_damage)
        enemy.cur_hp -= dmg
        menu.attack_message(dmg)

        self.images = []
        for i in range(6):
            self.images.append(pygame.transform.scale(load_image(
                f"..\data\pack_loreon_char_free\sword_1\\attack1_{i + 1}.png"), (1000, 500)))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(-50, -50, 100, 100)

        menu.wait(0.5)

        if enemy.cur_hp > 0:
            enemy.attack(menu, self)
        else:
            menu.win_message(self)

    def items(self):
        pass

    def end(self):
        global quit
        quit = True


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name):
        super(Enemy, self).__init__()

        self.name = name
        if name == 'imp_red':
            self.max_hp = 30
            self.cur_hp = 30
            self.min_damage = 7
            self.max_damage = 13
            self.money = 50
        else:
            self.max_hp = 100
            self.cur_hp = 100
            self.min_damage = 11
            self.max_damage = 16
            self.money = 300

        self.images = []
        self.index = 0

        hp_bar = ProgressBar(screen, 750, 100, 300, 40, lambda: self.cur_hp / self.max_hp, completedColour=(255, 0, 0))

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.images = []
            for i in range(6):
                self.images.append(pygame.transform.flip(pygame.transform.scale(load_image(
                    f'..\data\imp_axe_demon\{self.name}\idle_{i}.png'), (500, 350)), True, False))
            self.index = 0
            self.rect = pygame.Rect(650, 100, 100, 100)
        self.image = self.images[self.index]

    def attack(self, menu, player):
        dmg = randint(self.min_damage, self.max_damage)
        player.cur_hp -= dmg
        menu.damaged_message(dmg)

        self.images = []
        for i in range(6):
            self.images.append(pygame.transform.flip(pygame.transform.scale(load_image(
                f"..\data\imp_axe_demon\{self.name}\\attack1_{i + 1}.png"), (1000, 500)), True, False))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(300, -50, 100, 100)

        menu.wait(0.5)

        if player.cur_hp <= 0:
            menu.wait(0.5)
            menu.defeat_message(player)


class Menu:
    def __init__(self, player, enemy, attack, items, retreat):
        self.player = player
        self.enemy = enemy
        self.attack = attack
        self.items = items
        self.retreat = retreat
        self.heal_potion = Button(
            screen, width * 0.6, 476, width * 0.4 - 22, 50, text='Зелье лечения',
            fontSize=height // 15, textHAlign='left', textVAlign='Bottom', margin=20,
            inactiveColour=(0, 0, 0),
            pressedColour=(127, 127, 127),
            textColour=(255, 255, 255),
            onClick=lambda: self.use_item_message()
        )
        self.heal_potion.hide()
        self.start()

    def message(self, text, n_string=0):
        font = pygame.font.Font(None, height // 15)
        text = font.render(text, True, (255, 255, 255))
        text_x = width - text.get_width() - 40
        text_y = height * 0.65 + height * n_string // 15 + 20
        screen.blit(text, (text_x, text_y))

    def start(self):
        self.message('Вы встретили противника!')

    def update(self):
        pygame.draw.rect(screen, (255, 255, 255), (10, height * 0.65 - 5, width - 20, height * 0.35 - 5), 5)
        pygame.draw.rect(screen, (255, 255, 255), (20, height * 0.65 + 5, width // 4, height * 0.1), 3)
        pygame.draw.rect(screen, (255, 255, 255), (20, height * 0.75 + 10, width // 4, height * 0.1), 3)
        pygame.draw.rect(screen, (255, 255, 255), (20, height * 0.85 + 15, width // 4, height * 0.1), 3)

    def attack_message(self, dmg):
        if self.heal_potion.isVisible():
            self.heal_potion.hide()
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.message('Вы атаковали противника!')
        self.message(f'Вы нанесли противнику {dmg} урона!', 1)
        self.update()

    def damaged_message(self, dmg):
        self.message('Противник атакует вас!', 2)
        self.message(f'Вы получили {dmg} урона!', 3)
        self.update()

    def items_message(self):
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.heal_potion.show()
        self.update()

    def use_item_message(self):
        self.heal_potion.hide()
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.player.cur_hp += 20
        self.message('Вы использовали зелье лечения!')
        self.message('Вы восстановили 20 единиц здоровья!', 1)
        self.update()
        self.wait(1)
        self.enemy.attack(self, self.player)

    def wait(self, time):
        self.attack.disable()
        self.items.disable()
        self.retreat.disable()
        for i in range(int(time * 12)):
            events = pygame.event.get()
            screen.fill((0, 0, 0), pygame.Rect(0, 0, width, height * 0.65))
            self.update()
            all_sprites = pygame.sprite.Group(self.player, self.enemy)
            all_sprites.update()
            all_sprites.draw(screen)
            pygame_widgets.update(events)
            pygame.display.flip()
            clock.tick(fps)
        self.attack.enable()
        self.items.enable()
        self.retreat.enable()

    def defeat_message(self, player):
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.message('Вы проиграли!')
        self.update()
        self.wait(1)
        player.end()

    def win_message(self, player):
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.message('Вы победили!')
        self.message('Вы получили 50 монет!', 1)
        self.update()
        self.wait(1)
        player.end()


def main(name):
    player = Player()
    enemy = Enemy(name)
    all_sprites = pygame.sprite.Group(player, enemy)
    attack = Button(
        screen, 23, 476, 314, 66, text='Attack',
        fontSize=65, margin=20,
        inactiveColour=(0, 0, 0),
        pressedColour=(127, 127, 127),
        textColour=(255, 255, 255),
        onClick=lambda: player.attack(menu, enemy)
    )
    items = Button(
        screen, 23, 553, 314, 66, text='Items',
        fontSize=65, margin=20,
        inactiveColour=(0, 0, 0),
        pressedColour=(127, 127, 127),
        textColour=(255, 255, 255),
        onClick=lambda: menu.items_message()
    )
    retreat = Button(
        screen, 23, 630, 314, 66, text='Retreat',
        fontSize=65, margin=20,
        inactiveColour=(0, 0, 0),
        pressedColour=(127, 127, 127),
        textColour=(255, 255, 255),
        onClick=lambda: print('Click')
    )
    menu = Menu(player, enemy, attack, items, retreat)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or quit == True:
                running = False

        screen.fill((0, 0, 0), pygame.Rect(0, 0, width, height * 0.65))
        menu.update()
        all_sprites.update()
        all_sprites.draw(screen)
        pygame_widgets.update(events)
        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main('imp_red')
