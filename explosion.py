import pygame
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, color=(200, 200, 200), num_particles=20, lifetime=0.5, radius_factor=1.0):
        super().__init__()
        self.particles = []
        self.position = pygame.Vector2(position)
        self.color = color
        self.lifetime = lifetime
        self.age = 0

        # Generate particles
        for _ in range(num_particles):
            speed = random.uniform(50, 150) * radius_factor
            angle = random.uniform(0, 360)
            velocity = pygame.Vector2(0, -1).rotate(angle) * speed
            radius = random.randint(2, 5) * radius_factor
            self.particles.append({"pos": self.position.copy(), "vel": velocity, "radius": radius})

    def update(self, dt):
        self.age += dt
        for p in self.particles:
            p["pos"] += p["vel"] * dt
        if self.age >= self.lifetime:
            self.kill()

    def draw(self, screen):
        # Create transparent surface for fading
        surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        alpha = max(0, 255 * (1 - self.age / self.lifetime))  # Fade out
        for p in self.particles:
            color = (*self.color, int(alpha))
            pygame.draw.circle(surf, color, (int(p["pos"].x), int(p["pos"].y)), int(p["radius"]))
        screen.blit(surf, (0, 0))

