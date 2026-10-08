import math
import random

import pygame


class EnergyOrb:
    def __init__(self, width):
        self.radius = 10
        self.x = random.randint(self.radius, width - self.radius)
        self.y = -self.radius
        self.vx = random.uniform(-0.6, 0.6)
        self.vy = random.uniform(0.4, 0.8)
        self.phase = random.uniform(0, math.tau)

    def update(self, width):
        self.x += self.vx
        self.y += self.vy
        self.phase += 0.08

        if self.x <= self.radius or self.x >= width - self.radius:
            self.vx *= -1

    def off_screen(self, height):
        return self.y > height + self.radius

    def collides(self, rect):
        closest_x = max(rect.left, min(self.x, rect.right))
        closest_y = max(rect.top, min(self.y, rect.bottom))
        dx = self.x - closest_x
        dy = self.y - closest_y
        return dx * dx + dy * dy <= self.radius * self.radius

    def draw(self, screen):
        pulse = 2 + int((math.sin(self.phase) + 1) * 2)
        center = (int(self.x), int(self.y))

        pygame.draw.circle(
            screen,
            (80, 220, 255),
            center,
            self.radius + pulse,
            2,
        )
        pygame.draw.circle(
            screen,
            (120, 240, 255),
            center,
            self.radius,
        )
        pygame.draw.circle(
            screen,
            (235, 255, 255),
            center,
            self.radius // 2,
        )
