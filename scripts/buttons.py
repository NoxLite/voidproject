import pygame
pygame.init()
font = pygame.font.Font(None, 32)


class Button():
    def __init__(self, x, y, width, height, color='#487fd9', text='', mode=''):
        super().__init__()
        self.x = x
        self.y = y
        self.size = (width, height)
        self.color = color
        self.is_clicked = False
        self.text = font.render(text, True, 'black')
        self.mode = mode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, *self.size))
        screen.blit(self.text, (self.x + 10, self.y + 15))

    def get_pressed_info(self, pos_mouse):
        if self.x <= pos_mouse[0] <= self.x + self.size[0] and self.y <= pos_mouse[1] <= self.y + self.size[1]:
            self.is_clicked = True
        else:
            self.is_clicked = False
