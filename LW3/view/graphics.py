import pygame
from pygame import Surface, Rect, Color, Vector2


def rotate_image(image, pos, origin_relative, angle) -> (Surface, Rect):
    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - origin_relative[0], pos[1] - origin_relative[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    return rotated_image, rotated_image_rect