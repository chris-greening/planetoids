import math

def calculate_collision_distance(bullet, asteroid):
    dist = math.sqrt((bullet.x - asteroid.x)**2 + (bullet.y - asteroid.y)**2)
    return dist