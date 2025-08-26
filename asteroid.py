import pygame
import random
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # Random gray-brown color
        base_gray = random.randint(100, 160)
        brown = random.randint(60, 100)
        self.color = (base_gray, base_gray - brown // 2, base_gray - brown)
        
        # Generate rough polygon offsets
        self.offsets = []
        points = max(6, int(self.radius / 2))
        for _ in range(points):
            offset = pygame.Vector2(random.uniform(-self.radius/3, self.radius/3),
                                    random.uniform(-self.radius/3, self.radius/3))
            self.offsets.append(offset)

    def draw(self, screen):
        # Draw an irregular polygon for the asteroid
        points = []
        for i in range(len(self.offsets)):
            angle = (i / len(self.offsets)) * 360
            point = pygame.Vector2(0, -self.radius).rotate(angle) + self.offsets[i] + self.position
            points.append((point.x, point.y))
        pygame.draw.polygon(screen, self.color, points, 2)

    def update(self, dt):
        self.position += self.velocity * dt

        # Wrap around screen horizontally
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        # Wrap around screen vertically
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)
        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = a * 1.2
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = b * 1.2

