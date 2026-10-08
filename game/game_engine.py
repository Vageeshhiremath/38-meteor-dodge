import pygame
import random

from game.ship import Ship
from game.meteor import Meteor
from game.laser import Laser
from game.energy_orb import EnergyOrb


WIDTH, HEIGHT = 700, 520
FPS = 60
BG = (8, 5, 20)
SHIELD_DURATION = FPS * 10
MULTIPLIER_INTERVAL = FPS * 10
MAX_MULTIPLIER = 5


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Meteor Dodge")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 26, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 46, bold=True)

        self.stars = [
            (
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.randint(1, 3),
            )
            for _ in range(80)
        ]

        self.reset()

    def reset(self):
        self.ship = Ship(WIDTH // 2, HEIGHT - 80)
        self.meteors = []
        self.lasers = []
        self.energy_orb = None
        self.powerup_timer = random.randint(300, 600)
        self.shield_timer = 0
        self.timer = 0
        self.survival_frames = 0
        self.multiplier_timer = 0
        self.multiplier = 1
        self.spawn_interval = 60
        self.score = 0
        self.game_over = False
        self.started = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    elif not self.started:
                        self.started = True
                    else:
                        self.lasers.append(Laser(*self.ship.rect.midtop))

        return True

    def update(self):
        if self.game_over or not self.started:
            return

        self.survival_frames += 1
        self.multiplier_timer += 1

        if (
            self.multiplier_timer >= MULTIPLIER_INTERVAL
            and self.multiplier < MAX_MULTIPLIER
        ):
            self.multiplier += 1
            self.multiplier_timer = 0

        keys = pygame.key.get_pressed()
        self.ship.move(keys, WIDTH, HEIGHT)

        self.timer += 1

        if self.timer >= self.spawn_interval:
            self.meteors.append(Meteor(WIDTH))
            self.timer = 0
            self.spawn_interval = max(20, self.spawn_interval - 0.3)

        if self.energy_orb is None:
            self.powerup_timer -= 1

            if self.powerup_timer <= 0:
                self.energy_orb = EnergyOrb(WIDTH)
                self.powerup_timer = random.randint(600, 900)
        else:
            self.energy_orb.update(WIDTH)

            if self.energy_orb.collides(self.ship.rect):
                self.shield_timer = SHIELD_DURATION
                self.energy_orb = None
            elif self.energy_orb.off_screen(HEIGHT):
                self.energy_orb = None

        if self.shield_timer > 0:
            self.shield_timer -= 1

        for laser in self.lasers:
            laser.update()

        safe_meteors = []

        for meteor in self.meteors:
            meteor.update()

            if meteor.collides(self.ship.rect):
                if self.shield_timer > 0:
                    self.shield_timer = 0
                    continue

                self.game_over = True
                self.multiplier = 1
                self.multiplier_timer = 0

            safe_meteors.append(meteor)

        self.meteors = safe_meteors

        remaining_meteors = []

        for meteor in self.meteors:
            hit = any(
                laser.rect.collidepoint(
                    int(meteor.x),
                    int(meteor.y),
                )
                for laser in self.lasers
            )

            if not hit:
                remaining_meteors.append(meteor)
            else:
                remaining_meteors.extend(meteor.split())

        self.meteors = remaining_meteors
        self.lasers = [
            laser for laser in self.lasers
            if not laser.off_screen()
        ]
        self.meteors = [
            meteor for meteor in self.meteors
            if not meteor.off_screen(HEIGHT)
        ]

        self.score += self.multiplier

    def draw(self):
        self.screen.fill(BG)

        for sx, sy, sr in self.stars:
            pygame.draw.circle(
                self.screen,
                (200, 200, 220),
                (sx, sy),
                sr,
            )

        for meteor in self.meteors:
            meteor.draw(self.screen)

        if self.energy_orb is not None:
            self.energy_orb.draw(self.screen)

        for laser in self.lasers:
            laser.draw(self.screen)

        self.ship.draw(self.screen)

        if self.shield_timer > 0:
            pygame.draw.circle(
                self.screen,
                (90, 220, 255),
                self.ship.rect.center,
                30,
                3,
            )

        score_text = self.font.render(
            f"Time: {self.survival_frames // 60}s",
            True,
            (200, 200, 240),
        )
        self.screen.blit(score_text, (10, 10))

        multiplier_text = self.font.render(
            f"x{self.multiplier}",
            True,
            (255, 220, 100),
        )
        self.screen.blit(
            multiplier_text,
            (WIDTH - multiplier_text.get_width() - 10, 10),
        )

        if not self.started:
            message = self.font.render(
                "Press SPACE to launch",
                True,
                (180, 180, 240),
            )
            self.screen.blit(
                message,
                (
                    WIDTH // 2 - message.get_width() // 2,
                    HEIGHT // 2,
                ),
            )

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            message = self.big_font.render(
                "DESTROYED!",
                True,
                (220, 80, 60),
            )
            submessage = self.font.render(
                f"Survived {self.survival_frames // 60}s | SPACE to Restart",
                True,
                (200, 200, 200),
            )

            self.screen.blit(
                message,
                (
                    WIDTH // 2 - message.get_width() // 2,
                    HEIGHT // 2 - 40,
                ),
            )
            self.screen.blit(
                submessage,
                (
                    WIDTH // 2 - submessage.get_width() // 2,
                    HEIGHT // 2 + 20,
                ),
            )

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
