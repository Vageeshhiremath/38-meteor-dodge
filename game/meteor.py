import pygame
import random
import math


LARGE_RADIUS = 20


class Meteor:
    def __init__(
        self,
        width=None,
        x=None,
        y=None,
        radius=None,
        vx=None,
        vy=None,
        color=None,
    ):
        self.x = random.randint(0, width) if x is None else x
        self.y = -30 if y is None else y
        self.radius = random.randint(12, 28) if radius is None else radius

        if vx is None or vy is None:
            angle = random.uniform(70, 110)
            speed = random.uniform(2, 5)
            self.vx = math.cos(math.radians(angle)) * speed
            self.vy = math.sin(math.radians(angle)) * speed
        else:
            self.vx = vx
            self.vy = vy

        if color is None:
            color = (
                random.randint(160, 220),
                random.randint(80, 120),
                random.randint(40, 80),
            )

        self.color = color
        self.rot = 0
        self.rot_speed = random.uniform(-3, 3)

    def split(self):
        if self.radius < LARGE_RADIUS:
            return []

        child_radius = max(8, self.radius // 2)
        child_count = random.randint(2, 3)
        direction = math.atan2(self.vy, self.vx)
        children = []

        for index in range(child_count):
            spread = math.radians(random.uniform(25, 55))

            if index % 2:
                spread *= -1

            angle = direction + spread
            speed = random.uniform(2.5, 4.5)

            children.append(
                Meteor(
                    x=self.x,
                    y=self.y,
                    radius=child_radius,
                    vx=math.cos(angle) * speed,
                    vy=math.sin(angle) * speed,
                    color=self.color,
                )
            )

        return children

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rot = (self.rot + self.rot_speed) % 360

    def off_screen(self, height):
        return self.y > height + 60

    def collides(self, rect):
        cx, cy = rect.centerx, rect.centery
        dx, dy = self.x - cx, self.y - cy
        return (dx**2 + dy**2) ** 0.5 < self.radius + 16

    def draw(self, screen):
        pts = []

        for i in range(7):
            angle = math.radians(self.rot + i * (360 / 7))
            r = self.radius * (0.8 + 0.2 * (i % 2))
            pts.append(
                (
                    int(self.x + r * math.cos(angle)),
                    int(self.y + r * math.sin(angle)),
                )
            )

        pygame.draw.polygon(screen, self.color, pts)

        inner = [
            (
                int(
                    self.x
                    + (self.radius * 0.5)
                    * math.cos(math.radians(self.rot + i * (360 / 7)))
                ),
                int(
                    self.y
                    + (self.radius * 0.5)
                    * math.sin(math.radians(self.rot + i * (360 / 7)))
                ),
            )
            for i in range(7)
        ]

        pygame.draw.polygon(
            screen,
            tuple(max(0, c - 40) for c in self.color),
            inner,
        )
