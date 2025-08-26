import pygame
from shot import Shot

class Weapon:
    def __init__(self, owner, shots_group, drawable_group, cooldown=0.3, shot_speed=500, shot_count=1, spread_angle=0):
        """
        owner: the Player instance
        shots_group: the pygame sprite group for shots
        drawable_group: the group for drawing shots
        cooldown: seconds between shots
        shot_speed: pixels per second
        shot_count: number of bullets per shot
        spread_angle: total spread in degrees for multiple bullets
        """
        self.owner = owner
        self.shots_group = shots_group
        self.drawable_group = drawable_group
        self.cooldown = cooldown
        self.shot_speed = shot_speed
        self.shot_count = shot_count
        self.spread_angle = spread_angle
        self.timer = 0

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt

    def shoot(self, shots_group=None, drawable_group=None):
        if self.timer > 0:
            return
        self.timer = self.cooldown
        base_rotation = self.owner.rotation

        # If no groups passed, use stored ones
        if shots_group is None:
            shots_group = self.shots_group
        if drawable_group is None:
            drawable_group = self.drawable_group

        for i in range(self.shot_count):
            angle_offset = 0
            if self.shot_count > 1:
                angle_offset = (-self.spread_angle/2) + i * (self.spread_angle/(self.shot_count-1))
            
            shot = Shot(self.owner.position.x, self.owner.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(base_rotation + angle_offset) * self.shot_speed
            shots_group.add(shot)
            drawable_group.add(shot)


