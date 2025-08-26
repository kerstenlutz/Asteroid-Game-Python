import pygame
from constants import *
from circleshape import CircleShape

class PowerUp(CircleShape):
    # Define possible power-up types and their colors
    COLORS = {
        "shield": (0, 255, 255),
        "triple_shot": (255, 0, 0),
        "rapid_fire": (255, 165, 0),
    }

    RADIUS = 15

    def __init__(self, position, kind):
        # Accept either a Vector2 or a tuple for position
        if isinstance(position, pygame.Vector2):
            x, y = position.x, position.y
        elif isinstance(position, tuple) or isinstance(position, list):
            x, y = position
        else:
            raise TypeError("position must be a Vector2 or a tuple/list of length 2")

        super().__init__(x, y, self.RADIUS)
        self.kind = kind
        self.color = self.COLORS.get(kind, (255, 255, 255))
        # Optional velocity for floating effect
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        # Optional: draw kind letter inside circle
        font = pygame.font.SysFont(None, 20)
        text = font.render(self.kind[0].upper(), True, (0, 0, 0))
        rect = text.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(text, rect)

    def update(self, dt):
        self.position += self.velocity * dt
        # Wrap around screen edges
        if self.position.x < 0: self.position.x = SCREEN_WIDTH
        if self.position.x > SCREEN_WIDTH: self.position.x = 0
        if self.position.y < 0: self.position.y = SCREEN_HEIGHT
        if self.position.y > SCREEN_HEIGHT: self.position.y = 0

    def collides_with(self, other):
        return self.position.distance_to(other.position) <= self.radius + other.radius





