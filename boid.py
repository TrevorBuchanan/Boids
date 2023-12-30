import math
import random


# Calculate unit vector
def normalize(vect2d):
    x = vect2d[0]
    y = vect2d[1]
    hypotenuse = math.sqrt(x * x + y * y)
    if hypotenuse == 0:
        hypotenuse = 1
    return [x / hypotenuse, y / hypotenuse]


# Calculate distance between 2 points
def dist(pt1, pt2):
    x_dist = pt1[0] - pt2[0]
    y_dist = pt1[1] - pt2[1]
    return math.sqrt(x_dist * x_dist + y_dist * y_dist)


class Boid:
    def __init__(self, b_id, max_vel, boundary):
        self.boid_id = b_id
        self.speed = random.randint(3, max_vel)
        self.boundary = boundary

        self.direction = [0, 0]
        self.position = self.generate_pos()
        self.color = self.generate_col()

        self.align_view_range = 50
        self.align_weakness = 1

        self.cohesion_view_range = 50
        self.cohesion_weakness = 120

        self.separation_view_range = 20
        self.separation_weakness = 11

        self.boids_in_range = []

    # Returns a random position within the boundaries O(1)
    def generate_pos(self):
        x = random.randint(0, self.boundary.width)
        y = random.randint(0, self.boundary.height)
        return [x, y]

    # Returns a color tuple according to boid_id O(1)
    def generate_col(self):
        if self.boid_id % 255 < 100:
            return math.floor((self.boid_id + 10) % 255) / 2, math.floor((self.boid_id + 10) % 255) / 3, math.floor(
                (self.boid_id + 100) % 255)
        return math.floor(self.boid_id % 255) / 2, math.floor(self.boid_id % 255) / 3, math.floor(
            self.boid_id % 255)

    # Calculate boids in the furthest view range of alignment, cohesion, and separation
    def boids_in_furthest_view_range(self, boids, start, end):
        self.boids_in_range = []
        max_view_range = max(self.align_view_range, self.cohesion_view_range, self.separation_view_range)
        for boid in boids[start:end]:
            if self.boid_id != boid.boid_id and dist(self.position, boid.position) < max_view_range:
                self.boids_in_range.append(boid)

    # Returns a random direction O(1)
    def random_dir(self):
        x_vel = random.random()
        y_vel = random.random()
        x_positive_dir = random.getrandbits(1)
        y_positive_dir = random.getrandbits(1)
        if x_positive_dir == 1:
            x_vel = -x_vel
        if y_positive_dir == 1:
            y_vel = -y_vel
        result_dir = normalize([x_vel, y_vel])
        result_dir[0] *= self.speed
        result_dir[1] *= self.speed
        return result_dir

    # Returns the final calculated direction from 3 boid rules (alignment, cohesion, separation) O(n)
    def calculate_dir(self, boids):
        self.boids_in_range = []
        self.boids_in_furthest_view_range(boids, 0, len(boids) - math.floor(len(boids)/2))
        # self.boids_in_furthest_view_range(boids, 0, len(boids))

        result_dir = [0, 0]
        align_dir = self.align()  # O(n)
        result_dir[0] += align_dir[0] / self.align_weakness
        result_dir[1] += align_dir[1] / self.align_weakness
        cohesion_dir = self.cohesion()  # O(n)
        result_dir[0] += cohesion_dir[0] / self.cohesion_weakness
        result_dir[1] += cohesion_dir[1] / self.cohesion_weakness
        separation_dir = self.separation()  # O(n)
        result_dir[0] += separation_dir[0] / self.separation_weakness
        result_dir[1] += separation_dir[1] / self.separation_weakness

        result_dir = normalize([result_dir[0], result_dir[1]])  # O(1)
        result_dir[0] *= self.speed
        result_dir[1] *= self.speed
        return result_dir

    # Align boid with boids in view range O(n)
    def align(self):
        desired_dir = [0, 0]
        total = 0
        # Loop through all boids to check if in view range and average their directions
        for boid in self.boids_in_range:
            if self.boid_id != boid.boid_id and dist(self.position, boid.position) < self.align_view_range:
                desired_dir[0] += boid.direction[0]
                desired_dir[1] += boid.direction[1]
                total += 1

        # If no boid in view range, continue in direction
        if total == 0:
            return self.direction

        # If boids found in view range, steer towards average
        if total > 0:
            desired_dir[0] = desired_dir[0] / total
            desired_dir[1] = desired_dir[1] / total
            desired_dir[0] += self.direction[0]
            desired_dir[1] += self.direction[1]

        result_dir = normalize([desired_dir[0], desired_dir[1]])
        result_dir[0] *= self.speed
        result_dir[1] *= self.speed
        return result_dir

    # Steer boids towards center of boids in view range O(n)
    def cohesion(self):
        desired_dir = [0, 0]
        desired_pos = [0, 0]
        total = 0
        # Loop through all boids to check if in view range and average their directions
        for boid in self.boids_in_range:
            if self.boid_id != boid.boid_id and dist(self.position, boid.position) < self.cohesion_view_range:
                desired_pos[0] += boid.position[0]
                desired_pos[1] += boid.position[1]
                total += 1

        # If no boid in view range, continue in direction
        if total == 0:
            return self.direction

        # If boids found in view range, steer towards average
        if total > 0:
            desired_pos[0] = desired_pos[0] / total
            desired_pos[1] = desired_pos[1] / total

            desired_dir[0] = desired_pos[0] - self.position[0]
            desired_dir[1] = desired_pos[1] - self.position[1]
        return desired_dir

    # Steer boids away from boids in view range that are too close O(n)
    def separation(self):
        desired_dir = [0, 0]
        desired_pos = [0, 0]
        total = 0
        # Loop through all boids to check if in view range and average their directions
        for boid in self.boids_in_range:
            if self.boid_id != boid.boid_id and dist(self.position, boid.position) < self.separation_view_range:
                desired_pos[0] += boid.position[0]
                desired_pos[1] += boid.position[1]
                total += 1

        # If no boid in view range, continue in direction
        if total == 0:
            return self.direction

        # If boids found in view range, steer towards average
        if total > 0:
            desired_pos[0] = desired_pos[0] / total
            desired_pos[1] = desired_pos[1] / total

            desired_dir[0] = self.position[0] - desired_pos[0]
            desired_dir[1] = self.position[1] - desired_pos[1]
        return desired_dir

    # Move the boid according to current situation and handle border O(n)
    def move(self, boids):
        if self.direction == [0, 0]:
            self.direction = self.random_dir()  # O(1)
            self.position[0] += self.direction[0]
            self.position[1] += self.direction[1]
        else:
            self.direction = self.calculate_dir(boids)  # O(n)
            self.position[0] += self.direction[0]
            self.position[1] += self.direction[1]

        # Border control
        if self.position[0] < 0:  # Too far left
            self.position[0] = self.boundary.width
        elif self.position[0] > self.boundary.width:  # Too far right
            self.position[0] = 0

        if self.position[1] < 0:  # Too far up
            self.position[1] = self.boundary.height
        elif self.position[1] > self.boundary.height:  # Too far down
            self.position[1] = 0
