import pygame
import sys
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from powerup import PowerUp
from weapon import Weapon

def load_high_score(file="highscore.txt"):
    try:
        with open(file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "AAAA 0"

def save_high_score(initials, score, file="highscore.txt"):
    with open(file, "w") as f:
        f.write(f"{initials} {score}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    # Load background
    background = pygame.image.load("images/9659.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Initialize game variables
    score = 0
    lives = 3
    respawn_timer = 0
    font = pygame.font.SysFont(None, 36)

    # Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    # Containers
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    PowerUp.containers = (powerups, updatable, drawable)

    # Asteroid field
    asteroid_field = AsteroidField()

    # Player
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shots_group=shots, drawable_group=drawable)

    # Weapons
    single_shot = Weapon(player, shots, drawable, cooldown=0.3, shot_speed=500, shot_count=1)
    triple_spread = Weapon(player, shots, drawable, cooldown=0.5, shot_speed=400, shot_count=3, spread_angle=30)
    rapid_fire = Weapon(player, shots, drawable, cooldown=0.1, shot_speed=350, shot_count=1)
    player.weapon = single_shot

    # Load high score
    try:
        with open("highscore.txt", "r") as f:
            high_score, initials = f.read().split(",")
            high_score = int(high_score)
    except:
        high_score, initials = 0, "---"

    # Game loop
    dt = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        updatable.update(dt)
        explosions.update(dt)
        powerups.update(dt)

        if respawn_timer > 0:
            respawn_timer -= dt

        # Player collisions
        if respawn_timer <= 0:
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    if player.shield_timer <= 0:
                        lives -= 1
                        if lives <= 0:
                            running = False
                        else:
                            player.position = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                            player.velocity = pygame.Vector2(0,0)
                            player.rotation = 0
                            respawn_timer = INVINCIBILITY_DURATION

        # Shot hits asteroid
        for shot in shots:
            for asteroid in asteroids:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    score += 10

                    radius_factor = asteroid.radius / ASTEROID_MIN_RADIUS
                    num_particles = int(20 * radius_factor)
                    explosion = Explosion(asteroid.position, num_particles=num_particles, radius_factor=radius_factor)
                    explosions.add(explosion)

                    # Random power-up drop
                    if random.random() < 0.1:  # 10% chance
                        kind = random.choice(["triple", "rapid", "shield"])
                        powerup = PowerUp(asteroid.position, kind)
                        powerups.add(powerup)

        # Player picks up power-ups
        for powerup in powerups:
            if powerup.collides_with(player):
                if powerup.kind == "triple":
                    player.weapon = triple_spread
                    player.weapon_timer = 10.0
                elif powerup.kind == "rapid":
                    player.weapon = rapid_fire
                    player.weapon_timer = 10.0
                elif powerup.kind == "shield":
                    player.shield_timer = 10.0
                powerup.kill()

        # Reset weapon after power-up expires
        if player.weapon_timer <= 0:
            player.weapon = single_shot
        else:
            player.weapon_timer -= dt

        # Render
        screen.blit(background, (0,0))
        for e in explosions:
            e.draw(screen)
        for obj in drawable:
            obj.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)

        # HUD
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Lives: {lives}", True, (255,255,255))
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
        highscore_text = font.render(f"High Score: {high_score} ({initials})", True, (255,255,0))
        screen.blit(highscore_text, (SCREEN_WIDTH//2 - 100, 10))

        # Power-up timers
        if player.weapon_timer > 0:
            timer_text = font.render(f"Power-Up: {int(player.weapon_timer)}s", True, (0, 255, 0))
            screen.blit(timer_text, (10, 50))
        if player.shield_timer > 0:
            shield_text = font.render(f"Shield: {int(player.shield_timer)}s", True, (0, 255, 255))
            screen.blit(shield_text, (10, 80))

        pygame.display.flip()
        dt = clock.tick(60)/1000

    # Game Over
    screen.fill((0,0,0))
    gameover_text = font.render("GAME OVER", True, (255,0,0))
    final_score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(gameover_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 30))
    screen.blit(final_score_text, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 + 10))
    pygame.display.flip()
    pygame.time.wait(3000)

    # Update high score
    if score > high_score:
        initials_input = input("Enter your 4-letter initials: ")[:4]
        with open("highscore.txt", "w") as f:
            f.write(f"{score},{initials_input}")

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()





