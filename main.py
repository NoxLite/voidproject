import pygame
from scripts.random_generation import random_generation
from scripts.buttons import Button

pygame.init()


def game():
    global map, running
    board = Board(map)
    while running:
        screen.fill('black')
        board.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    running = False
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
                for elem in buttons:
                    elem.get_pressed_info(event.pos)
                    elem.function()
        if map[player.x][player.y] in ['e', 'd']:
            player.x, player.y = 0, 0
        if map[player.x][player.y] == 'sd':
            map[player.x][player.y] = 'd'
            player.x, player.y = 0, 0
        for elem in buttons:
            elem.draw(screen)
        pygame.display.flip()


class Escape(Button):
    def function(self):
        global running
        if self.is_clicked:
            running = False


class Regeneration(Button):
    def function(self):
        global map, player
        if self.is_clicked:
            map = rework()
            player.x, player.y = (0, 0)


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


def rework():
    random_generation()
    with open('maps/RandomMap.txt') as f:
        m = [elem.split(' ') for elem in f.read().split('\n')]
    return m


map = rework()
player = Player(0, 0)
buttons = [Escape(230, 160, 200, 50, text='Выход'), Regeneration(230, 100, 200, 50, text='Регенерация')]
if __name__ == '__main__':
    running = True
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    game()
    pygame.quit()