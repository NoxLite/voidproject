import pygame
from scripts.random_generation import random_generation
from scripts.buttons import Button
pygame.init()
font = pygame.font.Font(None, 32)
processes = [1, 0, 0, 0]
current_version = 'start'

with open(r'changelogs\info.txt') as f:
    all_versions = [elem for elem in f.read().split()]


def game():
    global map, running
    board = Board(map)
    while processes[0]:
        screen.fill('black')
        board.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    for i in range(len(processes)):
                        processes[i] = 0
                if event.key == 119:
                    if player.x != 0 and map[player.x - 1][player.y] not in ['b']:
                        player.x -= 1
                if event.key == 97 and map[player.x][player.y - 1] not in ['b']:
                    if player.y != 0:
                        player.y -= 1
                if event.key == 115:
                    if player.x != 14 and map[player.x + 1][player.y] not in ['b']:
                        player.x += 1
                if event.key == 100:
                    if player.y != 14 and map[player.x][player.y + 1] not in ['b']:
                        player.y += 1
                if event.key == 109:
                    map = rework()
                    player.x, player.y = 0, 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for elem in buttons_game:
                        elem.get_pressed_info(event.pos)
                        elem.function()
        if map[player.x][player.y] in ['e', 'd']:
            player.x, player.y = 0, 0
        if map[player.x][player.y] == 'sd':
            map[player.x][player.y] = 'd'
            player.x, player.y = 0, 0
        for elem in buttons_game:
            elem.draw(screen)
        pygame.display.flip()


def change_log_window():
    y_text = 10
    up_y = 10
    min_y = 10 + 40 * 21
    can_moved = False
    while processes[1]:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    for i in range(len(processes)):
                        processes[i] = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [4, 5] and can_moved:
                    if event.button == 4:
                        if y_text > min_y:
                            y_text -= 10
                    if event.button == 5:
                        if y_text < up_y:
                            y_text += 10
                if event.button == 1:
                    for elem in buttons_change_log:
                        elem.get_pressed_info(event.pos)
                        elem.function()
                        if elem.is_clicked:
                            y_text = 10
        pygame.draw.line(screen, 'blue', (300,0), (300, 1080), 4)
        info = open(f'changelogs/{current_version}.txt', mode='r', encoding="utf-8").read().split('\n')
        min_y = 10 - len(info) * 40 + 22 * 40
        if len(info) > 21:
            can_moved = True
        for i in range(len(info)):
            text = font.render(info[i], True, 'white')
            screen.blit(text, (310, y_text + 40 * i))
        for elem in buttons_change_log:
            elem.draw(screen)
        pygame.display.flip()


class Escape(Button):
    def function(self):
        global running
        if self.is_clicked:
            for i in range(len(processes)):
                processes[i] = 0
            if self.mode == 'game':
                processes[0] = 1
            self.is_clicked = False


class Regeneration(Button):
    def function(self):
        global map, player
        if self.is_clicked:
            map = rework()
            player.x, player.y = (0, 0)
            self.is_clicked = False


class ChangeLogButton(Button):
    def function(self):
        if self.is_clicked:
            global processes
            processes[0] = 0
            processes[1] = 1
            self.is_clicked = False



class Board():
    def __init__(self, map):
        self.x = len(map[0])
        self.y = len(map)

    def draw(self, screen):
        global player
        player_x, player_y = player.get_coord()
        for i in range(0, self.x):
            for j in range(0, self.y):
                if map[j][i] in ['*', 'sd']:
                    pygame.draw.rect(screen, 'white', (440 + i * 40, 100 + j * 40, 40, 40), 1)
                elif map[j][i] == 'b':
                    pygame.draw.rect(screen, 'red', (440 + i * 40, 100 + j * 40, 40, 40))
                elif map[j][i] == 'e':
                    pygame.draw.rect(screen, 'green', (440 + i * 40, 100 + j * 40, 40, 40))
                elif map[j][i] == 'd':
                    pygame.draw.rect(screen, 'yellow', (440 + i * 40, 100 + j * 40, 40, 40))
                if (j, i) == (player_x, player_y):
                    pygame.draw.circle(screen, 'blue', (460 + i * 40, 120 + j * 40), 18)


class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coord(self):
        return self.x, self.y


class Version(Button):
    def function(self):
        if self.is_clicked:
            global current_version
            current_version = self.mode
            self.is_clicked = False


def rework():
    random_generation()
    with open('maps/RandomMap.txt') as f:
        m = [elem.split(' ') for elem in f.read().split('\n')]
    return m


map = rework()
player = Player(0, 0)
buttons_game = [Escape(130, 160, 300, 50, text='Выход', mode='all'),
                Regeneration(130, 100, 300, 50, text='Регенерация'),
                ChangeLogButton(130, 220, 300, 50, text='Список изменений')]
buttons_change_log = [Escape(10, 10, 280, 50, text='Назад', mode='game'),
                      Version(10, 70, 280, 50, text='Стартовая страница', mode=all_versions[0])]
for i in range(1, len(all_versions)):
    buttons_change_log.append(Version(10, 70 + i * 50 + 10 * i, 280, 50, text=all_versions[i], mode=all_versions[i]))

if __name__ == '__main__':
    running = True
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    while 1 in processes:
        if processes[0]:
            game()
        if processes[1]:
            change_log_window()
    pygame.quit()