# example comment to show Taylor how github updates
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Load spaceship image
spaceship = pygame.image.load("spaceship.png")
spaceship = pygame.transform.scale(spaceship, (50, 50))
spaceship_rect = spaceship.get_rect()
spaceship_rect.topleft = (width // 2, height - 60)

# Bullet properties
bullet_width = 5
bullet_height = 10
bullet_speed = -10
bullets = []

# Asteroid properties
asteroid_width = 50
asteroid_height = 50
asteroid_speed = 5
asteroids = []

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font for displaying the score
font = pygame.font.SysFont(None, 36)
score = 0


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# Main game loop
running = True
while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_rect = pygame.Rect(
                    spaceship_rect.centerx - bullet_width // 2,
                    spaceship_rect.top,
                    bullet_width,
                    bullet_height,
                )
                bullets.append(bullet_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship_rect.left > 0:
        spaceship_rect.x -= 5
    if keys[pygame.K_RIGHT] and spaceship_rect.right < width:
        spaceship_rect.x += 5

    # Move bullets
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Create new asteroids
    if random.randint(1, 30) == 1:
        asteroid_rect = pygame.Rect(
            random.randint(0, width - asteroid_width),
            0,
            asteroid_width,
            asteroid_height,
        )
        asteroids.append(asteroid_rect)

    # Move asteroids
    for asteroid in asteroids[:]:
        asteroid.y += asteroid_speed
        if asteroid.y > height:
            asteroids.remove(asteroid)
        if spaceship_rect.colliderect(asteroid):
            pygame.quit()
            sys.exit()

    # Check for bullet collisions with asteroids
    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            if bullet.colliderect(asteroid):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                score += 10
                break

    # Draw everything
    screen.blit(spaceship, spaceship_rect)
    for bullet in bullets:
        pygame.draw.rect(screen, green, bullet)
    for asteroid in asteroids:
        pygame.draw.rect(screen, red, asteroid)
    draw_text(f"Score: {score}", font, white, screen, 10, 10)

    pygame.display.flip()
    clock.tick(60)
