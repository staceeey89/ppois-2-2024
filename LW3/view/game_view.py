import threading

import pygame
from pygame import Surface
from pygame.font import Font

from controller.event_listener import EventListener
from controller.event_manager import *
from model.game_model import GameModel
from model.game_state_machine import STATE_PLAY, STATE_HELP, STATE_MENU, STATE_GAME_OVER, STATE_RECORDS, \
    STATE_SAVE_RECORD
from model.repository import load_sprite, load_records


class AssteroidsView(EventListener):
    def __init__(self, event_manager, game_model):
        self.event_manager: EventBus = event_manager
        event_manager.register_listener(self)
        self.model: GameModel = game_model
        self.is_initialized: bool = False
        self.screen: Surface = None
        self.clock = None
        self.small_font: Font = None
        self.large_font: Font = None

        self.modifier_to_show: str | None = None
        self.modifier_shown = False

        self.selected_menu_option: int = 0
        self.current_menu_options: list = []
        self.records_list: list = []

        self.renderers = {
            STATE_MENU: self.render_menu,
            STATE_PLAY: self.render_play,
            STATE_HELP: self.render_help,
            STATE_RECORDS: self.render_records,
            STATE_GAME_OVER: self.render_game_over,
            STATE_SAVE_RECORD: self.render_save_record,
        }

    def notify(self, event):
        if isinstance(event, TickEvent):
            if not self.is_initialized:
                return

            current_state = self.model.state_stack.peek()
            self.renderers[current_state]()

            self.clock.tick(60)
        elif isinstance(event, ModifierAppliedEvent):
            self.modifier_shown = False
            self.modifier_to_show = event.modifier
        elif isinstance(event, StateChangeEvent):
            self.modifier_to_show = None
            if event.state == STATE_RECORDS:
                self.records_list = load_records()
        elif isinstance(event, QuitEvent):
            self.is_initialized = False
        elif isinstance(event, MenuItemSelectionChangedEvent):
            self.selected_menu_option += 1 if event.increase else -1
            self.selected_menu_option %= len(self.current_menu_options) if not len(self.current_menu_options) == 0 else 1
        elif isinstance(event, MenuItemSelectedEvent):
            if len(self.current_menu_options) > 0:
                self.event_manager.post(StateChangeEvent(self.current_menu_options[self.selected_menu_option][1]))
        elif isinstance(event, InitializeEvent):
            self.initialize()

    def render_menu(self):
        self.current_menu_options = [
            ("New game", STATE_PLAY),
            ("About game", STATE_HELP),
            ("Records table", STATE_RECORDS),
            ("Exit", None),
        ]
        self.screen.fill((0, 0, 0))

        for entity in self.model.get_game_objects():
            entity.draw(self.screen)

        welcome_label = self.large_font.render(
            'Welcome to Asteroids',
            True, (255, 255, 255))
        self.screen.blit(welcome_label, (100, 100))

        for index, option in enumerate(self.current_menu_options):
            selected = index == self.selected_menu_option
            color = (0, 100, 200) if selected else (0, 40, 80)
            option_text = self.small_font.render(option[0], True, color)

            pos_y = 200 + index * 40
            self.screen.blit(option_text, (100, pos_y))

            if selected:
                pygame.draw.rect(self.screen, color, pygame.Rect(100 - 10, pos_y, 2, 20))

        pygame.display.flip()

    def render_play(self):
        self.screen.fill((20, 20, 50))

        for entity in self.model.get_game_objects():
            entity.draw(self.screen)

        self._render_game_interface(self.screen)

        pygame.display.flip()

    def render_help(self):
        self.screen.fill((0, 0, 0))

        welcome_label = self.large_font.render(
            'About the game',
            True, (255, 255, 255))
        self.screen.blit(welcome_label, (100, 100))

        rules_y_offset = 0
        for line in ["Rules of this infinite game are simple.",
                     "You are playing for spaceship.",
                     "You must destroy asteroids before they destroy you.",
                     "You can encounter UFOs. They want to kill you.",
                     "If you kill UFO, there's 50% chance for random modifier:",
                     "Slowdown for asteroids, Speed shooting or Extra live.",
                     "Only asteroids and enemies can kill you.",
                     "Use LEFT, RIGHT to rotate spaceship, UP to accelerate, SPACE to shoot.",
                     "Good luck, comrade."]:
            about_label = self.small_font.render(line, True, (255, 255, 255))
            self.screen.blit(about_label, (100, 200 + rules_y_offset))
            rules_y_offset += about_label.get_height() + 5

        continue_label = self.small_font.render(
            'Press SPACE, ENTER or ESC to return to menu.',
            True, (255, 255, 255))
        self.screen.blit(continue_label, (100, 200 + rules_y_offset + 50))

        pygame.display.flip()

    def render_records(self):
        self.screen.fill((0, 0, 0))

        records_header_label = self.large_font.render(
            'Records table',
            True, (255, 255, 255))
        self.screen.blit(records_header_label, (100, 100))

        for index, record in enumerate(self.records_list):
            record_str = str(index + 1) + '. ' + record[0] + ' - ' + str(record[1])
            record_label = self.small_font.render(record_str, True, (255, 255, 255))
            self.screen.blit(record_label, (100, 200 + index * 40))

        continue_label = self.small_font.render(
            'Press SPACE, ENTER or ESC to return to menu.',
            True, (255, 255, 255))
        self.screen.blit(continue_label, (100, 250 + len(self.records_list) * 40))

        pygame.display.flip()

    def render_game_over(self):
        self.current_menu_options = [
            ("Back to menu", None),
            ("Records table", STATE_RECORDS),
        ]
        self.screen.fill((0, 0, 0))

        game_over_text = self.large_font.render(
            'Game over',
            True, (255, 255, 255))
        self.screen.blit(game_over_text, (100, 100))

        score_text = self.large_font.render(
            'Your score is ' + str(self.model.score),
            True, (255, 255, 255))
        self.screen.blit(score_text, (100, 150))

        for index, option in enumerate(self.current_menu_options):
            selected = index == self.selected_menu_option
            color = (0, 100, 200) if selected else (0, 40, 80)
            option_text = self.small_font.render(option[0], True, color)

            pos_y = 250 + index * 40
            self.screen.blit(option_text, (100, pos_y))

            if selected:
                pygame.draw.rect(self.screen, color, pygame.Rect(100 - 10, pos_y, 2, 20))

        pygame.display.flip()

    def render_save_record(self):
        self.screen.fill((0, 0, 0))

        record_set_header_label = self.large_font.render(
            'You died. But with an honour!',
            True, (255, 255, 255))
        self.screen.blit(record_set_header_label, (100, 100))

        score_text = self.small_font.render(
            'Your score: ' + str(self.model.score),
            True, (255, 255, 255))
        self.screen.blit(score_text, (100, 200))

        score_text = self.small_font.render(
            'Enter your name to save the record:',
            True, (255, 255, 255))
        self.screen.blit(score_text, (100, 250))

        entry_pos_y = 300

        option_text = self.small_font.render(self.model.player_name, True, (255, 255, 255))
        self.screen.blit(option_text, (100, entry_pos_y))

        pos_x = 100 + option_text.get_width() + 2

        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(pos_x, entry_pos_y, 2, 20))

        pygame.display.flip()

    def initialize(self):
        pygame.init()
        pygame.mixer.music.load("assets/sounds/background.mp3")
        pygame.mixer.music.play(loops=True)
        pygame.font.init()
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.small_font = pygame.font.Font(None, 30)
        self.large_font = pygame.font.Font(None, 60)
        self.is_initialized = True

    def _reset_modifier_to_show(self):
        self.modifier_to_show = None

    def _render_game_interface(self, surface):
        spaceship_sprite = load_sprite("spaceship", size=(45, 45))
        lives_bar_x = 100
        lives_bar_y = 30

        if self.modifier_to_show:
            if not self.modifier_shown:
                self.modifier_shown = True
                t = threading.Timer(5, self._reset_modifier_to_show)
                t.start()

            modifier_label = self.small_font.render(self.modifier_to_show, True, (255, 255, 255))
            self.screen.blit(modifier_label, (self.screen.get_width() / 2 - modifier_label.get_width() / 2,
                                              lives_bar_y + modifier_label.get_height() / 2))

        score_label = self.large_font.render(str(self.model.score), True, (255, 255, 255))
        self.screen.blit(score_label, (self.screen.get_width() - score_label.get_width() - 40, lives_bar_y))

        for i in range(0, self.model.lives):
            surface.blit(spaceship_sprite, (lives_bar_x + i * 50, lives_bar_y, 32, 32))
