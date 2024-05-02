import json
import os
from typing import Dict, List
from dataclasses import dataclass

from game.configs.config_paths import ConfigPaths


@dataclass
class EnemyData:
    sprite: str
    score: int
    weapon: str


@dataclass
class WeaponData:
    sprite: str
    speed: int
    advanced: bool
    sound: str


@dataclass
class WaveData:
    enemies: List[List[str]]


@dataclass
class AnimationData:
    sprite: str
    frame_duration: int


class JSONParser:
    def __init__(self, configs: ConfigPaths):
        self.__enemies_file = configs.enemies
        self.__weapons_file = configs.weapons
        self.__waves_file = configs.waves
        self.__animations_file = configs.animations

        self.enemies = self.__parse_enemies()
        self.weapons = self.__parse_weapons()
        self.__validate_enemies_weapons()
        self.waves = self.__parse_waves()
        self.__validate_waves()
        self.animations = self.__parse_animations()

    def __parse_enemies(self) -> Dict[str, EnemyData]:
        current_directory = os.getcwd()
        print("Текущая директория:", current_directory)
        with open(self.__enemies_file, 'r') as f:
            data = json.load(f)
            enemies_data = data['enemies']
            enemies = {}
            for enemy_name, enemy_info in enemies_data.items():
                enemy = EnemyData(enemy_info['sprite'], enemy_info['score'], enemy_info['weapon'])
                enemies[enemy_name] = enemy
            return enemies

    def __parse_weapons(self) -> Dict[str, WeaponData]:
        with open(self.__weapons_file, 'r') as f:
            data = json.load(f)
            weapons_data = data['weapons']
            weapons = {}
            for weapon_name, weapon_info in weapons_data.items():
                weapon = WeaponData(weapon_info['sprite'],
                                    weapon_info['speed'],
                                    weapon_info.get('advanced'),
                                    weapon_info.get('sound'))
                weapons[weapon_name] = weapon
            return weapons

    def __parse_waves(self):
        if self.enemies is not None:
            with open(self.__waves_file, 'r') as f:
                data = json.load(f)
                waves_data = data['waves']
                waves = []
                for wave in waves_data:
                    enemies_in_wave = []
                    for enemy_wave in wave:
                        enemy_types = enemy_wave['row']
                        enemies_in_wave.append(enemy_types)
                    waves.append(WaveData(enemies_in_wave))
                return waves
        else:
            raise ValueError("Cannot parse waves. Parse enemies first.")

    def __parse_animations(self) -> Dict[str, AnimationData]:
        with open(self.__animations_file, 'r') as f:
            data = json.load(f)
            animations_data = data['animations']
            animations = {}
            for animation_name, animation_info in animations_data.items():
                animation = AnimationData(animation_info['sprite'], animation_info['frame_duration'])
                animations[animation_name] = animation
            return animations

    def __validate_waves(self):
        enemies = self.enemies
        waves = self.waves
        enemy_names = enemies.keys()
        for wave in waves:
            for enemy_row in wave.enemies:
                for enemy_name in enemy_row:
                    if enemy_name not in enemy_names:
                        raise ValueError(f"Enemy '{enemy_name}' in waves is not defined in enemies.json.")

    def __validate_enemies_weapons(self):
        """
        Validate that enemies use only weapons that are defined in weapons data.
        """
        weapons_names = set(self.weapons.keys())
        for enemy_name, enemy_info in self.enemies.items():
            enemy_weapon = enemy_info.weapon
            if enemy_weapon not in weapons_names:
                raise ValueError(f"Weapon '{enemy_weapon}' for enemy '{enemy_name}' is not defined in weapons.")
