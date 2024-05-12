from model.entities.base_entity import BaseEntity


def process_collisions(entities: list[BaseEntity]):
    for ent1 in entities:
        for ent2 in entities:
            if ent1 != ent2 and ent1.collides_with(ent2):
                displacement = ent2.position - ent1.position

                if displacement.x == 0 and displacement.y == 0:
                    continue

                collision_normal = displacement.normalize()
                relative_velocity = ent2.velocity - ent1.velocity
                relative_speed_along_normal = relative_velocity.dot(collision_normal)

                if relative_speed_along_normal > 0:
                    continue

                # Impulse
                j = -2 * relative_speed_along_normal / (ent1.mass + ent2.mass)

                ent1.velocity -= j * collision_normal * ent2.mass
                ent2.velocity += j * collision_normal * ent1.mass

                # print(ent1.velocity, ent2.velocity)
