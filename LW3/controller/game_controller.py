import pygame
import model
from controller.event_listener import EventListener
from controller.event_manager import *
from model.game_state_machine import STATE_HELP, STATE_PLAY, STATE_MENU, STATE_GAME_OVER, STATE_RECORDS, \
    STATE_SAVE_RECORD


# Handler for input
class Keyboard(EventListener):
    def __init__(self, event_manager, game_model):
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.model = game_model

        self.handlers = {
            STATE_MENU: self.event_handler_menu,
            STATE_GAME_OVER: self.event_handler_menu,
            STATE_PLAY: self.event_handler_play,
            STATE_HELP: self.event_handler_info_page,
            STATE_RECORDS: self.event_handler_info_page,
            STATE_SAVE_RECORD: self.event_handler_save_record,
        }

    def notify(self, event):
        if isinstance(event, TickEvent):
            current_state = self.model.state_stack.peek()
            self.handlers[current_state]()

    # Handles input in main menu
    def event_handler_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event_manager.post(QuitEvent())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    self.event_manager.post(MenuItemSelectionChangedEvent(increase=True))

                elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    self.event_manager.post(MenuItemSelectionChangedEvent(increase=False))

                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.event_manager.post(MenuItemSelectedEvent())

    # Handles input in help state or records page
    def event_handler_info_page(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event_manager.post(QuitEvent())

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
                    self.event_manager.post(StateChangeEvent(None))

    # Handles input in game over state when game is best
    def event_handler_save_record(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event_manager.post(QuitEvent())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.event_manager.post(StateChangeEvent(None))
                elif (pygame.K_a <= event.key <= pygame.K_z
                      or event.key == pygame.K_SPACE
                      or pygame.K_0 <= event.key <= pygame.K_9):
                    self.model.player_name += chr(event.key)
                elif event.key == pygame.K_BACKSPACE:
                    self.model.player_name = self.model.player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.model.player_name != "":
                        self.model.save_record()
                        self.event_manager.post(StateChangeEvent(None))

    # Handles input in play state
    def event_handler_play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event_manager.post(QuitEvent())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.event_manager.post(StateChangeEvent(None))

                self.event_manager.post(InputEvent(event.unicode))

        is_key_pressed = pygame.key.get_pressed()

        if self.model.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.model.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.model.spaceship.rotate(clockwise=False)

            if is_key_pressed[pygame.K_SPACE]:
                self.model.spaceship.shoot()

            if is_key_pressed[pygame.K_UP]:
                self.model.spaceship.accelerate()
