import pygame
import json
from copy import deepcopy
from random import choice, randrange

W, H = 10, 20
TILE = 30
GAME_RES = W * TILE, H * TILE
RES = 500, 600
FPS = 60

pygame.init()

main_font = pygame.font.Font('resources/main_font.ttf', 65)
help_font = pygame.font.Font('resources/main_font.ttf', 30)

title_tetris = main_font.render("TETRIS", True, pygame.Color("darkorange"))
title_score = help_font.render("Score:", True, pygame.Color("lightblue"))
title_next_figure = help_font.render("Next figure:", True, pygame.Color("lightblue"))


sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

pygame.mixer.music.load("resources/tetris_theme.mp3")
pygame.mixer.music.play(-1)


def get_figures_configuration():
    with open("resources/figures_conf.json", "r") as json_file:
        data = json.load(json_file)

    figures_pos = [list(map(tuple, figure)) for figure in data]

    return figures_pos


def check_borders(figure, field, i):
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


# menu
def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(sc, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(sc, inactive_color, (x, y, width, height))

    text_surface = main_font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (x + W / 2, y + H / 2)
    sc.blit(text_surface, text_rect)


def save_record_to_json(name, score):
    with open("resources/records.json", 'r') as file:
        data = json.load(file)

    new_record = {"name": name, "score": score}

    data.append(new_record)

    with open("resources/records.json", 'w') as file:
        json.dump(data, file, indent=4)


def start_game():
    score = 0
    game_over = False
    scores, total_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}, 0
    anim_count, anim_speed, anim_limit = 0, 5, 2000

    figures_pos = get_figures_configuration()

    figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    field = [[0 for i in range(W)] for j in range(H)]

    figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))

    get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

    color, next_color = get_color(), get_color()

    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

    while True:

        dx, rotate = 0, False
        sc.fill(pygame.Color('white'))
        sc.blit(game_sc, (0, 0))
        game_sc.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    anim_limit = 200
                elif event.key == pygame.K_UP:
                    rotate = True

        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
            if not check_borders(figure, field, i):
                figure = deepcopy(figure_old)
                break

        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_borders(figure, field, i):
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break

        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders(figure, field, i):
                    figure = deepcopy(figure_old)
                    break

        line, total_lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                total_lines += 1

        if total_lines > 0:
            pygame.mixer.Sound("resources/stage_clear.mp3").play()
        score += scores[total_lines]

        [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(game_sc, color, figure_rect)

        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(game_sc, col, figure_rect)

        for i in range(4):
            figure_rect.x = next_figure[i].x * TILE + 255
            figure_rect.y = next_figure[i].y * TILE + 220
            pygame.draw.rect(sc, next_color, figure_rect)

        sc.blit(title_tetris, (320, 5))
        sc.blit(title_score, (320, 100))
        sc.blit(help_font.render(str(score), True, pygame.Color('red')), (400, 100))
        sc.blit(title_next_figure, (320, 150))

        for i in range(W):
            if field[0][i]:
                game_over = True

        if game_over:
            pygame.mixer.Sound("resources/game_over.mp3").play()
            block_tetris_game = True
            field = [[0 for j in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 5, 2000
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (0, 0))
                pygame.display.flip()
                clock.tick(200)

            if score > int(get_record_from_json()[0]['score']):
                input_text = ""
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                save_record_to_json(input_text, score)
                                score = 0
                                show_menu()
                            elif event.key == pygame.K_BACKSPACE:
                                input_text = input_text[:-1]
                            else:
                                if len(input_text) < 24:
                                    input_text += event.unicode
                    title_congratulations = main_font.render("NEW RECORD!", True, pygame.Color('red'))
                    title_name = help_font.render(input_text, True, pygame.Color("black"))
                    square_to_titles = pygame.Rect(0, 190, 500, 150)
                    pygame.draw.rect(sc, (255, 255, 255), square_to_titles)
                    sc.blit(title_congratulations, (100, 200))
                    input_rect = pygame.Rect(40, 275, 400, 50)
                    pygame.draw.rect(sc, (150, 150, 150), input_rect)
                    pygame.draw.rect(sc, (0, 0, 0), input_rect, 2)
                    sc.blit(title_name, (45, 290))
                    pygame.display.flip()
                    clock.tick()

            while block_tetris_game:
                score = 0
                game_over = False
                title_game_over = main_font.render("GAME OVER!", True, pygame.Color('red'))
                title_restart = help_font.render("Press R to restart", True, pygame.Color('blue'))
                title_quit = help_font.render("or Q to quit to the menu", True, pygame.Color('blue'))
                square_to_titles = pygame.Rect(0, 190, 500, 150)
                pygame.draw.rect(sc, (255, 255, 255), square_to_titles)
                sc.blit(title_game_over, (100, 200))
                sc.blit(title_restart, (100, 270))
                sc.blit(title_quit, (100, 305))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            block_tetris_game = False
                        elif event.key == pygame.K_q:
                            show_menu()

        pygame.display.flip()
        clock.tick()


def get_record_from_json():
    temp = []

    with open("resources/records.json", "r") as file:
        data = json.load(file)

    if isinstance(data, list):
        temp.extend(data)
    else:
        temp.append(data)
    return sorted(temp, key=lambda x: x.get("score", ""), reverse=True)[0:10]


def high_scores():

    sorted_data = get_record_from_json()

    print(sorted_data[0]['score'])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        sc.fill(pygame.Color("white"))
        text_y = 50
        for i, entry in enumerate(sorted_data, start=1):
            text_surface = help_font.render(f"{i}. {entry['name']}: {entry['score']}", True, pygame.Color('black'))
            text_rect = text_surface.get_rect(center=(RES[0] // 2, text_y))
            sc.blit(text_surface, text_rect)
            text_y += 40

        draw_button("Back to menu", RES[0]//2, 525, 400, 50, pygame.Color('green'), (150, 150, 150), show_menu)
        pygame.display.flip()
        clock.tick()


def game_rules():
    rules = [
        "Tetris Game Rules:",
        "- The objective is to fill horizontal lines on the board to make them disappear.",
        "- Tetrominoes fall from the top and can be rotated to fit into the right place.",
        "- The game ends when tetrominoes pile up and reach the top of the screen.",
        "- Use the arrow keys to move tetrominoes and the up key to rotate them.",
        "- Enjoy the game!"
    ]

    image_tetrominoes = pygame.image.load("resources/tetrominoes.png")
    scaled_image = pygame.transform.scale(image_tetrominoes, (300, 225))

    title_tetriminoes = help_font.render("Tetriminoes:", True, pygame.Color("black"))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            sc.fill(pygame.Color("white"))

            text_y = 50
            help_small_font = pygame.font.Font('resources/main_font.ttf', 17)
            for line in rules:
                text_surface = help_small_font.render(line, True, pygame.Color("black"))
                text_rect = text_surface.get_rect(topleft=(20, text_y))
                sc.blit(text_surface, text_rect)
                text_y += text_rect.height + 5

            sc.blit(scaled_image, (170, 200))
            sc.blit(title_tetriminoes, (20, 200))
            draw_button("Back to menu", RES[0]//2, 525, 400, 50, pygame.Color('green'), (150, 150, 150), show_menu)
            pygame.display.flip()
            clock.tick()


def quit_game():
    pygame.quit()
    exit()


def show_menu():
    while True:
        for event_in_menu in pygame.event.get():
            if event_in_menu.type == pygame.QUIT:
                pygame.quit()
                exit()

        sc.fill((255, 255, 255))

        draw_button("Start game", 200, 150, 400, 50, pygame.Color("red"), (150, 150, 150), start_game)
        draw_button("Records", 200, 250, 400, 50, pygame.Color("orange"), (150, 150, 150), high_scores)
        draw_button("Info", 200, 350, 400, 50, pygame.Color("green"), (150, 150, 150), game_rules)
        draw_button("Exit", 200, 450, 400, 50, pygame.Color("blue"), (150, 150, 150), quit_game)
        sc.blit(title_tetris, (170, 5))
        clock.tick()
        pygame.display.flip()


show_menu()
