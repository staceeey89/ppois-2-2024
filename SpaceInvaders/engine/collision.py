from typing import List

from engine.game_object import GameObject


def collision(objects_1: List[GameObject], objects_2: List[GameObject]):
    def decorator(func):
        def wrapper():
            for obj1 in objects_1:
                for obj2 in objects_2:
                    if obj2 is obj1:
                        continue
                    if obj1.rect.colliderect(obj2.rect):
                        result = func(obj1, obj2)
                        return result
            return None
        return wrapper
    return decorator


class Collision:
    @staticmethod
    def collision(f1, f2):
        def decorator(func):
            def wrapper(self=None):
                # try:
                objects_1 = f1(self)
                # except:
                #     objects_1 = f1
                # try:
                objects_2 = f2(self)
                # except:
                #     objects_2 = f2
                for obj1 in objects_1:
                    for obj2 in objects_2:
                        if obj2 is obj1:
                            continue
                        if obj1.rect.colliderect(obj2.rect):

                            result = func(self, obj1, obj2)
                            return result
                return None
            return wrapper
        return decorator
