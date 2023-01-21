import pygame
import os
import sys
import sqlite3
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
quit = False  # для выхода из игры
flag_lose = False


class Inventory:  # инвентарь
    def __init__(self, menu, player, enemy, cur):
        self.menu = menu
        self.player = player
        self.enemy = enemy

        inventory = cur.execute("""SELECT * FROM inventory""").fetchall()

        self.heal_potion = inventory[0][0]  # кол-во предметов из бд
        self.beer = inventory[0][1]
        self.bomb = inventory[0][1]

    def items_show(self):  # показывать доступные опции при нажатии на кнопку Предметы
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.menu.attack.disable()
        self.menu.items.disable()
        self.menu.retreat.disable()

        self.cancel_btn = Button(
            screen, width * 0.6, 476, width * 0.4 - 22, 50, text=f'Назад',
            fontSize=height // 15, textHAlign='left', textVAlign='Bottom', margin=20,
            inactiveColour=(0, 0, 0),
            pressedColour=(127, 127, 127),
            textColour=(255, 255, 255),
            onClick=lambda: self.cancel()
        )
        self.heal_potion_btn = Button(
            screen, width * 0.6, 476 + height // 15 + 5, width * 0.4 - 22, 50,
            text=f'Зелье лечения: {self.heal_potion}',
            fontSize=height // 15, textHAlign='left', textVAlign='Bottom', margin=20,
            inactiveColour=(0, 0, 0),
            pressedColour=(127, 127, 127),
            textColour=(255, 255, 255),
            onClick=lambda: self.use_heal_potion()
        )
        self.beer_btn = Button(
            screen, width * 0.6, 476 + (height * 2) // 15 + 10, width * 0.4 - 22, 50,
            text=f'Пиво: {self.beer}',
            fontSize=height // 15, textHAlign='left', textVAlign='Bottom', margin=20,
            inactiveColour=(0, 0, 0),
            pressedColour=(127, 127, 127),
            textColour=(255, 255, 255),
            onClick=lambda: self.use_beer()
        )
        self.bomb_btn = Button(
            screen, width * 0.6, 476 + (height * 3) // 15 + 15, width * 0.4 - 22, 50,
            text=f'Бомба: {self.bomb}',
            fontSize=height // 15, textHAlign='left', textVAlign='Bottom', margin=20,
            inactiveColour=(0, 0, 0),
            pressedColour=(127, 127, 127),
            textColour=(255, 255, 255),
            onClick=lambda: self.use_bomb()
        )

        if self.heal_potion <= 0:  # заблокировать предметы которые ззакончились
            self.heal_potion_btn.disable()
        if self.beer <= 0:
            self.beer_btn.disable()
        if self.bomb <= 0:
            self.bomb_btn.disable()

        self.menu.update()

    def cancel(self):  # выход из меню инвентаря
        self.hide()
        self.menu.attack.enable()
        self.menu.items.enable()
        self.menu.retreat.enable()

    def hide(self):  # спрятать кнопки при выходе из меню ивентаря
        self.cancel_btn.hide()
        self.heal_potion_btn.hide()
        self.beer_btn.hide()
        self.bomb_btn.hide()
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.menu.update()

    def use_heal_potion(self):  # использовать зелье лечения кеоторое лечит 20 хп
        self.hide()
        self.heal_potion -= 1
        self.player.cur_hp += 20
        if self.player.cur_hp > self.player.max_hp:
            self.player.cur_hp = self.player.max_hp
        self.menu.use_item_message('зелье лечения', 'восстановили 20 здоровья')

    def use_beer(self):  # использовать пиво которое увеличивает амплитуду урона
        self.hide()
        self.beer -= 1
        self.player.min_dmg -= 2
        self.player.max_dmg += 4
        self.menu.use_item_message('пиво', 'дезориентированы и злы')

    def use_bomb(self):  # использовать бомбу которая наносит 30 урона
        self.hide()
        self.bomb -= 1
        self.enemy.cur_hp -= 30
        self.menu.use_item_message('бомбу', 'сделали противнику больно')
        self.menu.wait(0.5)


class Player(pygame.sprite.Sprite):  # игрок
    def __init__(self, cur):
        super(Player, self).__init__()

        stats = cur.execute("""SELECT * FROM stats WHERE name = 'player'""").fetchall()

        self.max_hp = stats[0][1]  # статы из бд
        self.cur_hp = stats[0][2]
        self.min_dmg = stats[0][3]
        self.max_dmg = stats[0][4]
        self.money = stats[0][5]

        self.images = []
        self.index = 0

        hp_bar = ProgressBar(screen, 200, 100, 300, 40, lambda: self.cur_hp / self.max_hp, completedColour=(255, 0, 0))  # полоска хп

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

    def attack(self, menu, enemy):  # атака при нажатии на кнопку атаковать
        dmg = randint(self.min_dmg, self.max_dmg)
        enemy.cur_hp -= dmg
        menu.attack_message(dmg)

        self.images = []
        for i in range(6):  # анимация атаки
            self.images.append(pygame.transform.scale(load_image(
                f"..\data\pack_loreon_char_free\sword_1\\attack1_{i + 1}.png"), (1000, 500)))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(-50, -50, 100, 100)

        menu.wait(0.5)

        if enemy.cur_hp > 0:  # проверка на смерть противника
            enemy.attack(menu, self)
        else:
            self.money += enemy.money
            menu.win_message()
            enemy.cur_hp = enemy.max_hp

    def retreat(self, menu):  # отступить и потерять до 50 монет
        if self.money >= 50:
            drop = 50
        else:
            drop = self.money
        self.money -= drop
        menu.retreat_message(drop)
        global flag_lose
        flag_lose = True

    def end(self):  # окончание процесса боя
        global quit
        quit = True


class Enemy(pygame.sprite.Sprite):  # противник
    def __init__(self, name, cur):
        super(Enemy, self).__init__()

        self.name = name

        stats = cur.execute(f"""SELECT * FROM stats WHERE name = '{name}'""").fetchall()

        self.max_hp = stats[0][1]  # статы из бд в зависимости от имени
        self.cur_hp = stats[0][2]
        self.min_dmg = stats[0][3]
        self.max_dmg = stats[0][4]
        self.money = stats[0][5]

        self.images = []
        self.index = 0

        if name == 'imp_red':
            y = 100
        else:
            y = 20
        hp_bar = ProgressBar(screen, 760, y, 300, 40, lambda: self.cur_hp / self.max_hp, completedColour=(255, 0, 0))  # полоска хп

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.images = []
            if self.name == 'imp_red':  # от типа противника зависит его положение и скейл размеров спрайтов
                for i in range(6):
                    self.images.append(pygame.transform.flip(pygame.transform.scale(load_image(
                        f'..\data\imp_axe_demon\{self.name}\idle_{i}.png'), (500, 350)), True, False))
                self.rect = pygame.Rect(650, 100, 100, 100)
            else:
                for i in range(6):
                    self.images.append(pygame.transform.flip(pygame.transform.scale(load_image(
                        f'..\data\imp_axe_demon\{self.name}\idle_{i}.png'), (1000, 700)), True, False))
                self.rect = pygame.Rect(400, -220, 100, 100)
            self.index = 0
        self.image = self.images[self.index]

    def attack(self, menu, player):  # атака противника после каждого действия игрока
        dmg = randint(self.min_dmg, self.max_dmg)
        player.cur_hp -= dmg
        menu.damaged_message(dmg)

        self.images = []
        if self.name == 'imp_red':
            for i in range(6):  # анимация атаки
                self.images.append(pygame.transform.flip(pygame.transform.scale(load_image(
                    f"..\data\imp_axe_demon\{self.name}\\attack1_{i + 1}.png"), (1000, 500)), True, False))
            self.rect = pygame.Rect(300, -50, 100, 100)
        else:
            for i in range(6):  # анимация атаки
                self.images.append(pygame.transform.flip(pygame.transform.scale(load_image(
                    f"..\data\imp_axe_demon\{self.name}\\attack1_{i + 1}.png"), (1050, 570)), True, False))
            self.rect = pygame.Rect(368, -103, 100, 100)
        self.index = 0
        self.image = self.images[self.index]

        menu.wait(0.5)

        if player.cur_hp <= 0:  # проверка на смерть игрока
            menu.wait(0.5)
            menu.defeat_message()


class Menu:  # меню
    def __init__(self, player, enemy, attack, items, retreat):
        self.player = player
        self.enemy = enemy
        self.attack = attack
        self.items = items
        self.retreat = retreat
        self.start()

    def update(self):
        pygame.draw.rect(screen, (255, 255, 255), (10, height * 0.65 - 5, width - 20, height * 0.35 - 5), 5)
        pygame.draw.rect(screen, (255, 255, 255), (20, height * 0.65 + 5, width // 4, height * 0.1), 3)
        pygame.draw.rect(screen, (255, 255, 255), (20, height * 0.75 + 10, width // 4, height * 0.1), 3)
        pygame.draw.rect(screen, (255, 255, 255), (20, height * 0.85 + 15, width // 4, height * 0.1), 3)

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

    def message(self, text, n_string=0):  # для показа сообщений, номер строки влияет на положение сообщения по вертикали
        font = pygame.font.Font(None, height // 15)
        text = font.render(text, True, (255, 255, 255))
        text_x = width - text.get_width() - 40
        text_y = height * 0.65 + height * n_string // 15 + 20
        screen.blit(text, (text_x, text_y))

    def start(self):  # начальное сообщение
        self.message('Вы встретили противника!')

    def attack_message(self, dmg):  # сообщение о том что игрок атаковал противника
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.message('Вы атаковали противника!')
        self.message(f'Вы нанесли противнику {dmg} урона!', 1)
        self.update()

    def damaged_message(self, dmg):  # сообщение о получении игроком урона
        self.message('Противник атакует вас!', 2)
        self.message(f'Вы получили {dmg} урона!', 3)
        self.update()

    def use_item_message(self, item, effect):  # сообщение об использовании предмета
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.message(f'Вы использовали {item}!')
        self.message(f'Вы {effect}!', 1)
        self.update()
        self.wait(1)
        if self.enemy.cur_hp > 0:  # проверка на смерть противника (на случай использования бомбы)
            self.enemy.attack(self, self.player)
        else:
            self.player.money += self.enemy.money
            self.win_message()

    def defeat_message(self):  # сообщение о проигрыше игрока при его смерти
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.message('Вы проиграли!')
        self.update()
        self.wait(1)
        self.player.end()

    def win_message(self):  # сообщение о победе игрока
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.message('Вы победили!')
        self.message(f'Вы получили {self.enemy.money} монет!', 1)
        self.update()
        self.wait(1)
        self.player.end()

    def retreat_message(self, drop):  # сообщение о побеге игрока из боя
        screen.fill((0, 0, 0), pygame.Rect(0, height * 0.65, width, height))
        self.message('Вы решили отступить!')
        self.message(f'Вы потеряли {drop} монет!', 1)
        self.update()
        self.wait(1)
        self.player.end()


def main(name):  # игровой процесс, в name задается имя противника: 'imp_red' или 'demon_axe_red' (от этого зависят статы, спрайты и музыка)
    # if name == 'imp_red':
    #     pygame.mixer.music.load('..\data\Tooth and Claw.mp3')
    # else:
    #     pygame.mixer.music.load('..\data\Death or Sovngard.mp3')
    # pygame.mixer.music.play()
    # pygame.mixer.music.set_volume(0.5)

    con = sqlite3.connect("..\\data\\fight.db")  # работа с бд
    cur = con.cursor()

    player = Player(cur)
    enemy = Enemy(name, cur)
    all_sprites = pygame.sprite.Group(player, enemy)
    attack = Button(
        screen, 23, 476, 314, 66, text='Атаковать',
        fontSize=65, margin=20,
        inactiveColour=(0, 0, 0),
        pressedColour=(127, 127, 127),
        textColour=(255, 255, 255),
        onClick=lambda: player.attack(menu, enemy)
    )
    items = Button(
        screen, 23, 553, 314, 66, text='Предметы',
        fontSize=65, margin=20,
        inactiveColour=(0, 0, 0),
        pressedColour=(127, 127, 127),
        textColour=(255, 255, 255),
        onClick=lambda: inventory.items_show()
    )
    retreat = Button(
        screen, 23, 630, 314, 66, text='Отступить',
        fontSize=65, margin=20,
        inactiveColour=(0, 0, 0),
        pressedColour=(127, 127, 127),
        textColour=(255, 255, 255),
        onClick=lambda: player.retreat(menu)
    )
    menu = Menu(player, enemy, attack, items, retreat)
    inventory = Inventory(menu, player, enemy, cur)

    global quit
    global flag_lose
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # проверка на quit нужна для завершения боя
                running = False
            if quit:
                quit = False
                if flag_lose:
                    flag_lose = False
                    return True
                return False

        screen.fill((0, 0, 0), pygame.Rect(0, 0, width, height * 0.65))  # обновление экрана
        menu.update()
        all_sprites.update()
        all_sprites.draw(screen)
        pygame_widgets.update(events)
        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()


# if __name__ == '__main__':
#     main('imp_red')
#     main('demon_axe_red')
