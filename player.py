import pygame
from constants import *
from circleshape import CircleShape
from weapon import Weapon

class Player(CircleShape):
    def __init__(self, x, y, shots_group, drawable_group):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shots_group = shots_group
        self.drawable_group = drawable_group

        # Default weapon
        self.weapon = Weapon(self, shots_group=self.shots_group, drawable_group=self.drawable_group)

        # Shield timer
        self.shield_timer = 0.0
        self.weapon_timer = 0.0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        color = (0, 255, 255) if self.shield_timer > 0 else (255, 255, 255)
        pygame.draw.polygon(screen, color, self.triangle())
        if self.shield_timer > 0:
            pygame.draw.circle(screen, (0, 255, 255), (int(self.position.x), int(self.position.y)), self.radius + 5, 2)

    def rotate(self, dt, direction):
        self.rotation += PLAYER_TURN_SPEED * dt * direction

    def move(self, dt, forward=True):
        fwd = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += fwd * PLAYER_SPEED * dt * (1 if forward else -1)
        if self.position.x < 0: self.position.x = SCREEN_WIDTH
        if self.position.x > SCREEN_WIDTH: self.position.x = 0
        if self.position.y < 0: self.position.y = SCREEN_HEIGHT
        if self.position.y > SCREEN_HEIGHT: self.position.y = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.weapon.update(dt)

        if keys[pygame.K_a]:
            self.rotate(dt, -1)
        if keys[pygame.K_d]:
            self.rotate(dt, 1)
        if keys[pygame.K_w]:
            self.move(dt, True)
        if keys[pygame.K_s]:
            self.move(dt, False)
        if keys[pygame.K_SPACE]:
            self.weapon.shoot()

        # Update shield timer
        if self.shield_timer > 0:
            self.shield_timer -= dt

        # Revert weapon after timer ends
        if hasattr(self, "weapon_timer") and self.weapon_timer > 0:
            self.weapon_timer -= dt
            if self.weapon_timer <= 0:
                self.weapon = Weapon(self, self.shots_group, self.drawable_group,
                                     cooldown=0.3, shot_speed=500, shot_count=1)





