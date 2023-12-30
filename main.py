import pygame

from boid import Boid

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1435, 1000

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (10, 10, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.display.set_caption("Boids")
FPS = 50
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

boid_edge_radius = 7
boid_max_velocity = 6

BORDER = pygame.Rect(boid_edge_radius, boid_edge_radius, WIDTH, HEIGHT)


# Returns a type holding the orientation of a triangle according to its position and velocity
def calculate_orientation(pos, vector):
    return (pos[0] - vector[1] / 1.5, pos[1] + vector[0] / 1.5), \
        (pos[0] + vector[0] * 2, pos[1] + vector[1] * 2), \
        (pos[0] + vector[1] / 1.5, pos[1] - vector[0] / 1.5)


if __name__ == '__main__':
    clock = pygame.time.Clock()

    # Generate all boids
    boid_count = 1000
    boids = []
    for i in range(boid_count):
        boid = Boid(i, boid_max_velocity, BORDER)
        boids.append(boid)

    # Screen window loop
    running = True
    while running:
        # Set the frame rates
        clock.tick(FPS)

        # Check for closure
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        # Fill background
        screen.fill(DARK_BLUE)

        # # Draw and move boids
        for boid in boids:  # O(n^2)
            orientation = calculate_orientation(boid.position, boid.direction)  # O(1)
            pygame.draw.polygon(screen, boid.color, orientation)
            boid.move(boids)  # O(n)

        pygame.display.update()

pygame.quit()
