import pygame


SPEED = 8


class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 2, y - 18, 4, 18)

    def update(self):
        self.rect.y -= SPEED

    def off_screen(self):
        return self.rect.bottom < 0

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 220, 255), self.rect)
        pygame.draw.rect(screen, (220, 250, 255), self.rect.inflate(-2, 0))