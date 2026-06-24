import pygame
import sys
from enum import Enum
from mazegenerator.mazegenerator import MazeGenerator


class Dir(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

#def game():
#    while True:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                pygame.quit()
#                sys.exit()
#
#        screen.fill((40, 40, 40))
#
#        text = font.render("Game Started!", True, WHITE)
#        screen.blit(text, (250, 350))
#
#        pygame.display.update()
#

def dec_to_bin(dec: int, digs: int) -> str:
    res = ""
    while digs > 0:
        res = str(dec & 1) + res
        dec >>= 1
        digs -= 1
    return res


def start_screen(params: dict):

    x_size = params["x_size"]
    y_size = params["y_size"]
    screen = params["screen"]
    btnfont = params["btnfont"]
    pressed_btn = params["pressed_btn"]
    unpressed_btn = params["unpressed_btn"]
    white_col = params["white_col"]
    title_font = params["title_font"]

    x_spd = 0
    y_spd = 0
    x_pac = 8
    y_pac = 8
    pac_state = 0
    pac_dir = Dir.RIGHT

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    pac_dir = Dir.UP
                    x_spd = 0
                    y_spd = -4
                elif event.key == pygame.K_DOWN:
                    pac_dir = Dir.DOWN
                    x_spd = 0
                    y_spd = 4
                elif event.key == pygame.K_RIGHT:
                    pac_dir = Dir.RIGHT
                    x_spd = 4
                    y_spd = 0
                elif event.key == pygame.K_LEFT:
                    pac_dir = Dir.LEFT
                    x_spd = -4
                    y_spd = 0

        btn_Xstart = int(x_size * 0.45)
        btn_Ystart = int(y_size * 0.4)
        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()

        # screen.fill("#003049")
        play_button = pygame.Rect(btn_Xstart, btn_Ystart, 300, 75)
        score_button = pygame.Rect(btn_Xstart, btn_Ystart + 120, 300, 75)
        cont_button = pygame.Rect(btn_Xstart, btn_Ystart + 240, 300, 75)

        pac_image = pygame.image.load("resources/Pacman_HD.png").convert_alpha()
        red_ghost = pygame.image.load("resources/redgb.png").convert_alpha()
        blue_ghost = pygame.image.load("resources/bluegb.jpeg").convert_alpha()
        pac_dir_img = None
        match pac_dir:
            case Dir.UP:
                pac_dir_img = "up"
            case Dir.DOWN:
                pac_dir_img = "down"
            case Dir.RIGHT:
                pac_dir_img = "right"
            case Dir.LEFT:
                pac_dir_img = "left"

        match pac_state:
            case 0:
                pacman_surf = pygame.image.load(f"pacman-art/pacman-{pac_dir_img}/1.png").convert_alpha()
                pac_state = 1
            case 1:
                pacman_surf = pygame.image.load(f"pacman-art/pacman-{pac_dir_img}/2.png").convert_alpha()
                pac_state = 2
            case 2:
                pacman_surf = pygame.image.load(f"pacman-art/pacman-{pac_dir_img}/3.png").convert_alpha()
                pac_state = 0

        pacman_rect = pacman_surf.get_rect(center=(0, 0))

        resized_redG = pygame.transform.scale(red_ghost, (175, 175))
        resized_blueG = pygame.transform.scale(blue_ghost, (175, 175))
        resized_pac = pygame.transform.scale(pac_image, (200, 200))

        #pygame.Surface.set_colorkey(resized_redG, [0, 0, 0])
        #pygame.Surface.set_colorkey(resized_blueG, [0, 0, 0])
        #pygame.Surface.set_colorkey(resized_pac, [0, 0, 0])

        pygame.draw.rect(
            screen,
            unpressed_btn if play_button.collidepoint(mouse) else pressed_btn,
            play_button)
        pygame.draw.rect(
            screen,
            unpressed_btn if score_button.collidepoint(mouse) else pressed_btn,
            score_button)
        pygame.draw.rect(
            screen,
            unpressed_btn if cont_button.collidepoint(mouse) else pressed_btn,
            cont_button)

        title_1 = title_font.render("Pac", True, "yellow")
        title_2 = title_font.render("an", True, "yellow")
        tit1_h, _ = title_1.get_size()
        tit2_h, _ = title_2.get_size()
        play_text = btnfont.render("Start Game", True, white_col)
        score_text = btnfont.render("Score board", True, white_col)
        cont_text = btnfont.render("Controls", True, white_col)

        screen.blit(play_text, (btn_Xstart + 30, btn_Ystart + 35))
        screen.blit(score_text, (btn_Xstart + 30, btn_Ystart + 150))
        screen.blit(cont_text, (btn_Xstart + 50, btn_Ystart + 265))

        start = 500
        screen.blit(resized_pac, (start, 50))
        start += 201
        screen.blit(title_1, (start, 50))
        start += tit1_h + 2
        screen.blit(resized_redG, (start, 50))
        start += 176
        screen.blit(resized_blueG, (start, 50))
        start += 176
        screen.blit(title_2, (start, 50))

        screen.fill("#003049")
        grid = params["grid"]
        anchor = (600, 150)
        tile = 32
        y = 0
        for row in grid:
            x = 0
            for cell in row:
                if cell[3] == "1": # North
                    pygame.draw.line(screen,
                                    "white",
                                    (anchor[0] + x * tile, anchor[1] + y * tile),
                                    (anchor[0] + x * tile + tile, anchor[1] + y * tile),
                                    2
                    )
                if cell[2] == "1": # East
                    pygame.draw.line(screen,
                                    "white",
                                    (anchor[0] + x * tile + tile, anchor[1] + y * tile),
                                    (anchor[0] + x * tile + tile, anchor[1] + y * tile + tile),
                                    2
                    )
                if cell[1] == "1": # South
                    pygame.draw.line(screen,
                                    "white",
                                    (anchor[0] + x * tile, anchor[1] + y * tile + tile),
                                    (anchor[0] + x * tile + tile, anchor[1] + y * tile + tile),
                                    2
                    )
                if cell[0] == "1": # West
                    pygame.draw.line(screen,
                                    "white",
                                    (anchor[0] + x * tile, anchor[1] + y * tile),
                                    (anchor[0] + x * tile, anchor[1] + y * tile + tile)
                                    ,2
                    )
                x += 1
            y += 1
        x_pac += x_spd
        y_pac += y_spd
        pacman_rect.topleft = (anchor[0] + x_pac, anchor[1] + y_pac)
        screen.blit(pacman_surf, pacman_rect)

        pygame.display.flip()
        clock.tick(60)


def main_screen():
    pygame.init()
    x_size = 1920
    y_size = 1080
    screen = pygame.display.set_mode((x_size, y_size))
    pygame.display.set_caption("Start Menu Example")
    pygame.Color("#003049")
    maze = MazeGenerator()
    maze.generate()
    grid = [[dec_to_bin(y, 4) for y in x] for x in maze.maze]

    pressed_btn = (253, 216, 53)
    unpressed_btn = (251, 192, 45)
    white_col = (255, 255, 255)
    btnfont = pygame.font.SysFont(None, 60)
    title_font = pygame.font.SysFont(None, 200)
    params = {
        "x_size": x_size,
        "y_size": y_size,
        "screen": screen,
        "btnfont": btnfont,
        "title_font": title_font,
        "pressed_btn": pressed_btn,
        "unpressed_btn": unpressed_btn,
        "white_col": white_col,
        "grid": grid
    }
    start_screen(params)


if __name__ == "__main__":
    main_screen()
