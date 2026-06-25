import pygame
import sys
from enum import Enum
from mazegenerator.mazegenerator import MazeGenerator
from parser import Jsonparser


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


def collidePoint(rect: pygame.Rect, point: tuple) -> bool:
    if rect.right >= point[0] >= rect.left:
        if rect.bottom >= point[1] >= rect.top:
            return True
    return False


def collideRect(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    if (rect1.left <= rect2.right and rect2.left <= rect1.right and
        rect1.top <= rect2.bottom and rect2.top <= rect1.bottom):
        return True
    return False


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.x_size = 1920
        self.y_size = 1080
        self.screen = pygame.display.set_mode((self.x_size, self.y_size))
        
        self.pressed_btn = (253, 216, 53)
        self.unpressed_btn = (251, 192, 45)
        self.white_col = (255, 255, 255)
        self.btnfont = pygame.font.SysFont(None, 60)
        self.title_font = pygame.font.SysFont(None, 200)
        self.parser = Jsonparser("config.json")

    
    def main_menu(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        btn_Xstart = int(self.x_size * 0.45)
        btn_Ystart = int(self.y_size * 0.4)
        self.screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()

        play_button = pygame.Rect(btn_Xstart, btn_Ystart, 300, 75)
        score_button = pygame.Rect(btn_Xstart, btn_Ystart + 120, 300, 75)
        cont_button = pygame.Rect(btn_Xstart, btn_Ystart + 240, 300, 75)

        pac_image = pygame.image.load("resources/Pacman_HD.png").convert_alpha()
        red_ghost = pygame.image.load("resources/redgb.png").convert_alpha()
        blue_ghost = pygame.image.load("resources/bluegb.jpeg").convert_alpha()

        resized_redG = pygame.transform.scale(red_ghost, (175, 175))
        resized_blueG = pygame.transform.scale(blue_ghost, (175, 175))
        resized_pac = pygame.transform.scale(pac_image, (200, 200))

        pygame.draw.rect(
            self.screen,
            (self.unpressed_btn if play_button.collidepoint(mouse)
             else self.pressed_btn),
            play_button)
        pygame.draw.rect(
            self.screen,
            (self.unpressed_btn if score_button.collidepoint(mouse)
             else self.pressed_btn),
            score_button)
        pygame.draw.rect(
            self.screen,
            (self.unpressed_btn if cont_button.collidepoint(mouse)
             else self.pressed_btn),
            cont_button)

        title_1 = self.title_font.render("Pac", True, "yellow")
        title_2 = self.title_font.render("an", True, "yellow")
        tit1_h, _ = title_1.get_size()
        tit2_h, _ = title_2.get_size()
        play_text = self.btnfont.render("Start Game", True, self.white_col)
        score_text = self.btnfont.render("Score board", True, self.white_col)
        cont_text = self.btnfont.render("Controls", True, self.white_col)

        self.screen.blit(play_text, (btn_Xstart + 30, btn_Ystart + 35))
        self.screen.blit(score_text, (btn_Xstart + 30, btn_Ystart + 150))
        self.screen.blit(cont_text, (btn_Xstart + 50, btn_Ystart + 265))

        start = 500
        self.screen.blit(resized_pac, (start, 50))
        start += 201
        self.screen.blit(title_1, (start, 50))
        start += tit1_h + 2
        self.screen.blit(resized_redG, (start, 50))
        start += 176
        self.screen.blit(resized_blueG, (start, 50))
        start += 176
        self.screen.blit(title_2, (start, 50))

    def pacman(self):

        maze = MazeGenerator()
        maze.generate()
        grid = [[dec_to_bin(y, 4) for y in x] for x in maze.maze]
        print(grid)

        x_spd = 0
        y_spd = 0
        x_pac = 8
        y_pac = 8
        pac_state = 0
        pac_dir_img = None
        pac_dir = Dir.RIGHT

        x = (1960 - maze._width * 32) // 2
        y = (1080 - maze._height * 32) // 2
        anchor = (x, y)
        spawn = (x + 32 * 7, y + 32 * 6)
        mov_dir = None
        clock = pygame.time.Clock()
        while True:
            self.level(anchor, grid)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_4:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_UP:
                        mov_dir = Dir.UP
                    elif event.key == pygame.K_DOWN:
                        mov_dir = Dir.DOWN
                    elif event.key == pygame.K_RIGHT:
                        mov_dir = Dir.RIGHT
                    elif event.key == pygame.K_LEFT:
                        mov_dir = Dir.LEFT
            if (((spawn[0] + x_pac - anchor[0]) % 32 == 8) and
                    (spawn[1] + y_pac - anchor[1]) % 32 == 8):
                x_cell = (spawn[1] + y_pac - anchor[1]) // 32
                y_cell = (spawn[0] + x_pac - anchor[0]) // 32
                if mov_dir == Dir.LEFT and grid[x_cell][y_cell][0] == "0":
                    print("LEFT")
                    pac_dir = Dir.LEFT
                    x_spd = -1
                    y_spd = 0
                elif mov_dir == Dir.DOWN and grid[x_cell][y_cell][1] == "0":
                    print("DOWN")
                    pac_dir = Dir.DOWN
                    x_spd = 0
                    y_spd = 1
                elif mov_dir == Dir.RIGHT and grid[x_cell][y_cell][2] == "0":
                    print("RIGHT")
                    pac_dir = Dir.RIGHT
                    x_spd = 1
                    y_spd = 0
                elif mov_dir == Dir.UP and grid[x_cell][y_cell][3] == "0":
                    print("UP")
                    pac_dir = Dir.UP
                    x_spd = 0
                    y_spd = -1

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
                case 6:
                    pacman_surf = pygame.image.load(f"pacman-art/pacman-{pac_dir_img}/2.png").convert_alpha()
                case 12:
                    pacman_surf = pygame.image.load(f"pacman-art/pacman-{pac_dir_img}/3.png").convert_alpha()
            pac_state = (pac_state + 1) % 13

            pacman_rect = pacman_surf.get_rect()

            if (((spawn[0] + x_pac - anchor[0]) % 32 == 8) and
                    (spawn[1] + y_pac - anchor[1]) % 32 == 8):
                x_cell = (spawn[1] + y_pac - anchor[1]) // 32
                y_cell = (spawn[0] + x_pac - anchor[0]) // 32
                if pac_dir == Dir.LEFT and grid[x_cell][y_cell][0] == "1":
                    x_spd = 0
                    y_spd = 0
                elif pac_dir == Dir.DOWN and grid[x_cell][y_cell][1] == "1":
                    x_spd = 0
                    y_spd = 0
                elif pac_dir == Dir.RIGHT and grid[x_cell][y_cell][2] == "1":
                    x_spd = 0
                    y_spd = 0
                elif pac_dir == Dir.UP and grid[x_cell][y_cell][3] == "1":
                    x_spd = 0
                    y_spd = 0
            x_pac += x_spd
            y_pac += y_spd

            pacman_rect.topleft = (spawn[0] + x_pac,
                                   spawn[1] + y_pac)
            self.screen.blit(pacman_surf, pacman_rect)
            clock.tick(60)
            pygame.display.flip()

    def level(self, anchor: tuple[int, int], grid: list[list]) -> None:
        #lev_name, lev_size = self.parser.json_dict["levels&size"][level_number - 1]
        #print(lev_size)
        self.screen.fill("#003049")
        tile = 32
        y = 0
        for row in grid:
            x = 0
            for cell in row:
                if cell[0] == "1":  # West
                    pygame.draw.line(
                        self.screen,
                        "white",
                        (anchor[0] + x * tile, anchor[1] + y * tile),
                        (anchor[0] + x * tile, anchor[1] + y * tile + tile),
                        2
                    )
                if cell[1] == "1":  # South
                    pygame.draw.line(
                        self.screen,
                        "white",
                        (anchor[0] + x * tile, anchor[1] + y * tile + tile),
                        (anchor[0] + x * tile + tile,
                            anchor[1] + y * tile + tile),
                        2
                    )
                if cell[2] == "1":  # East
                    pygame.draw.line(
                        self.screen,
                        "white",
                        (anchor[0] + x * tile + tile, anchor[1] + y * tile),
                        (anchor[0] + x * tile + tile,
                            anchor[1] + y * tile + tile),
                        2
                    )
                if cell[3] == "1":  # North
                    pygame.draw.line(
                        self.screen,
                        "white",
                        (anchor[0] + x * tile, anchor[1] + y * tile),
                        (anchor[0] + x * tile + tile, anchor[1] + y * tile),
                        2
                    )
                x += 1
            y += 1








def main_screen():

    game = Game()
    while True:
        game.pacman()
        pygame.display.flip()



if __name__ == "__main__":
    main_screen()
