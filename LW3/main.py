import pygame

import controller.event_manager
import model.game_model
import view.game_view
import controller.game_controller

if __name__ == '__main__':
    pygame.display.set_caption("Asteroids")
    pygame.display.set_mode((1200, 800))
    pygame.mixer.init()

    event_manager = controller.event_manager.EventBus()
    game_model = model.game_model.GameModel(event_manager)
    keyboard = controller.game_controller.Keyboard(event_manager, game_model)
    graphics = view.game_view.AssteroidsView(event_manager, game_model)
    game_model.run()
