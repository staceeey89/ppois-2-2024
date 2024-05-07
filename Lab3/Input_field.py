import pygame
import sys


class Input_field:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.base_font = pygame.font.Font(None, 20)
        self.user_text = ""
        self.bg_block = pygame.Rect(500, 300, 150, 32)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.active = False

    def make_active(self):
        self.active = True
        self.color = self.color_active

    def make_disactive(self):
        self.active = False
        self.color = self.color_passive

    def update_text(self, event, sc):
        if event.type == pygame.KEYDOWN and self.active:
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:
                # get text input from 0 to -1 i.e. end.
                self.user_text = self.user_text[:-1]
            # formation
            else:
                # Check if the key is a letter
                if event.unicode.isalpha() and len(self.user_text) < 10:
                    # Add the letter to the user_text
                    self.user_text += event.unicode
        self.print_input(sc)

    # def fill_input(self, sc):
    #     while True:
    #         for event in pygame.event.get():
    #
    #             # if user types QUIT then the screen will close
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #
    #             if event.type == pygame.MOUSEBUTTONDOWN:
    #                 if not self.bg_block.collidepoint(event.pos):
    #                     self.make_disactive()
    #                     self.print_input(sc)
    #                     return pygame.mouse.get_pos()
    #
    #             if event.type == pygame.KEYDOWN and self.active:
    #                 # Check for backspace
    #                 if event.key == pygame.K_BACKSPACE:
    #                     # get text input from 0 to -1 i.e. end.
    #                     self.user_text = self.user_text[:-1]
    #                 # formation
    #                 else:
    #                     # Check if the key is a letter
    #                     if event.unicode.isalpha() and len(self.user_text) < 10:
    #                         # Add the letter to the user_text
    #                         self.user_text += event.unicode
    #         self.print_input(sc)

    def fill_input(self, sc):
        pass

    def print_input(self, sc):
        pygame.draw.rect(sc, self.color, self.bg_block)

        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))

        # render at position stated in arguments
        sc.blit(text_surface, (self.bg_block.x + 5, self.bg_block.y + 15))
        pygame.display.update()

    #def print_input(self, sc):
    #    #while True:
    #    for event in pygame.event.get():

            # if user types QUIT then the screen will close
    #        if event.type == pygame.QUIT:
    #            pygame.quit()
    #            sys.exit()

    #        if event.type == pygame.MOUSEBUTTONDOWN:
    #            if self.bg_block.collidepoint(event.pos):
    #                self.active = True
    #            else:
    #                self.active = False

    #        if event.type == pygame.KEYDOWN and self.active:
    #            # Check for backspace
    #            if event.key == pygame.K_BACKSPACE:
    #                # get text input from 0 to -1 i.e. end.xcvb
    #                self.user_text = self.user_text[:-1]
    #            # formation
    #            else:
    #                # Check if the key is a letter
    #                if event.unicode.isalpha() and len(self.user_text) < 10:
    #                    # Add the letter to the user_text
    #                    self.user_text += event.unicode

    #    # it will set background color of screen
    #    if self.active:
    #        self.color = self.color_active
    #    else:
    #        self.color = self.color_passive

            # draw rectangle and argument passed which should
        # be on screen
    #    pygame.draw.rect(sc, self.color, self.bg_block)

    #    text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))

        # render at position stated in arguments
    #    sc.blit(text_surface, (self.bg_block.x + 5, self.bg_block.y + 15))

        # set width of textfield so that text cannot get
        # outside of user's text input

        # display.flip() will update only a portion of the
        # screen to updated, not full area
    #    pygame.display.flip()

        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
    #    self.clock.tick(60)

