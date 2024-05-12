import random

from pygame import Vector2


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    speed = random.randrange(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)
