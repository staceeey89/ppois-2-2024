import pygame
import json
from pygame import Surface
from pygame.image import load
from pygame.mixer import Sound

MAX_RECORDS = 5
RECORDS_FILE = 'records.json'
CONFIG_FILE = 'config.json'


def load_sprite(name, with_alpha=True, size: tuple[int, int] | None = None) -> Surface:
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)
    loaded_sprite = pygame.transform.scale(loaded_sprite, size) if size is not None else loaded_sprite

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def load_sound(name):
    path = f"assets/sounds/{name}.mp3"
    return Sound(path)


def load_config() -> dict:
    try:
        f = open(CONFIG_FILE)
        return json.load(f)
    except:
        return {}


def load_records() -> list[tuple[str, int]]:
    try:
        f = open(RECORDS_FILE)
        return json.load(f)
    except:
        return []


def save_record(record: tuple[str, int]) -> None:
    new_records = [record]
    new_records.extend(load_records())
    new_records = new_records[:MAX_RECORDS]

    with open(RECORDS_FILE, "w") as write:
        json.dump(new_records, write)
    print(f"Saved object to {RECORDS_FILE}")
