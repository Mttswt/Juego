import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Configuration of the game window
window_size = (1300, 900)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Nave de Pygmies")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initial position and velocity of the ship
x, y = window_size[0] // 2, window_size[1] // 2
velocity = 0
max_velocity = 5
acceleration = 0.1
deceleration = 0.02

# Dimensions of the ship
ship_width, ship_height = 30, 30

# Initial angle and rotation speed of the ship
angle = 0
rotation_speed = 3

# Bounce off the screen edges function
def wrap_around(x, y):
    if x < -ship_width:
        x = window_size[0]
    elif x > window_size[0]:
        x = -ship_width
    if y < -ship_height:
        y = window_size[1]
    elif y > window_size[1]:
        y = -ship_height
    return x, y

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Control the ship
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle += rotation_speed
    if keys[pygame.K_RIGHT]:
        angle -= rotation_speed
    if keys[pygame.K_UP]:
        velocity += acceleration
        if velocity > max_velocity:
            velocity = max_velocity
    if keys[pygame.K_DOWN]:
        velocity -= acceleration
        if velocity < -max_velocity:
            velocity = -max_velocity

    # Decelerate when not accelerating
    if not (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
        if velocity > 0:
            velocity -= deceleration
            if velocity < 0:
                velocity = 0
        elif velocity < 0:
            velocity += deceleration
            if velocity > 0:
                velocity = 0

    # Update ship's position based on velocity and angle
    x += velocity * math.cos(math.radians(angle))
    y -= velocity * math.sin(math.radians(angle))

    # Wrap the ship around the screen edges
    x, y = wrap_around(x, y)

    # Draw the ship on the screen as an isosceles triangle with the point pointing forward
    screen.fill(WHITE)
    vertices = [
        (x, y - 15),       # Top vertex (point)
        (x - 15, y + 15),  # Bottom-left vertex
        (x + 15, y + 15)   # Bottom-right vertex
    ]
    rotated_vertices = [(v[0] - x, v[1] - y) for v in vertices]
    rotated_vertices = [(v[0] * math.cos(math.radians(angle)) - v[1] * math.sin(math.radians(angle)),
                         v[0] * math.sin(math.radians(angle)) + v[1] * math.cos(math.radians(angle))) for v in rotated_vertices]
    rotated_vertices = [(v[0] + x, v[1] + y) for v in rotated_vertices]
    pygame.draw.polygon(screen, BLUE, rotated_vertices)
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()