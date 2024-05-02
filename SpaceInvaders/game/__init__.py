import json
import pygame

from engine.dispatcher import Dispatcher
from game.configs.config_paths import ConfigPaths
from game.score_manager import ScoreManager
from parser import EnemyData, JSONParser, WaveData, WeaponData

CONFIG = 'configs/config.json'

with open(CONFIG, 'r') as f:
    config_data = json.load(f)

constants = config_data['constants']
paths = config_data['paths']
images = config_data['images']
sounds = config_data['sounds']
font_config = config_data['font']

SCREEN_WIDTH = constants['SCREEN_WIDTH']
SCREEN_HEIGHT = constants['SCREEN_HEIGHT']
WHITE = constants['WHITE']
BLACK = constants['BLACK']
GREEN = constants['GREEN']
RED = constants['RED']
BLUE = constants['BLUE']
PLAYER_WIDTH = constants['PLAYER_WIDTH']
PLAYER_HEIGHT = constants['PLAYER_HEIGHT']
ENEMY_WIDTH = constants['ENEMY_WIDTH']
ENEMY_HEIGHT = constants['ENEMY_HEIGHT']
BULLET_WIDTH = constants['BULLET_WIDTH']
BULLET_HEIGHT = constants['BULLET_HEIGHT']
BULLET_EXPLOSION_WIDTH = constants['BULLET_EXPLOSION_WIDTH']
BULLET_EXPLOSION_HEIGHT = constants['BULLET_EXPLOSION_HEIGHT']
BRICK_WIDTH = constants['BRICK_WIDTH']
BRICK_HEIGHT = constants['BRICK_HEIGHT']
SPACING = constants['SPACING']
FPS = constants['FPS']
CAPTION = constants['CAPTION']


config_paths = ConfigPaths(paths['enemies'],
                           paths['weapons'],
                           paths['waves'],
                           paths['animations']
                           )
scores_path = paths['scores']

# enemies_path = config_paths.enemies
# weapons_path = config_paths.weapons
# waves_path = config_paths.waves
# animations_path = config_paths.animations

player_img = images['player']
brick_img = images['brick']

ENEMY_SHOT = pygame.USEREVENT + 1
PAUSE = pygame.USEREVENT + 2
FLAGSHIP = pygame.USEREVENT + 3

parser = JSONParser(config_paths)
enemies = parser.enemies
weapons = parser.weapons
waves = parser.waves
animations = parser.animations

scores_manager = ScoreManager(scores_path)

pygame.init()
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(font_config['font_family'], font_config['font_size'])

sound = pygame.mixer.Sound(sounds['music'])
sound.play()

dp = Dispatcher(screen, FPS)
