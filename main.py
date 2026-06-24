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
        self.x_spd = 0
        self.y_spd = 0
        self.x_pac = 8
        self.y_pac = 8
        self.pac_state = 0
        self.pac_dir_img = None
        self.pac_dir = Dir.RIGHT
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
    
    def level(self, level_number: str = 1) -> None:
        #lev_name, lev_size = self.parser.json_dict["levels&size"][level_number - 1]
        #print(lev_size)
        maze = MazeGenerator((15, 15))
        maze.generate()
        grid = [[dec_to_bin(y, 4) for y in x] for x in maze.maze]

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
                        self.pac_dir = Dir.UP
                        self.x_spd = 0
                        self.y_spd = -2
                    elif event.key == pygame.K_DOWN:
                        self.pac_dir = Dir.DOWN
                        self.x_spd = 0
                        self.y_spd = 2
                    elif event.key == pygame.K_RIGHT:
                        self.pac_dir = Dir.RIGHT
                        self.x_spd = 2
                        self.y_spd = 0
                    elif event.key == pygame.K_LEFT:
                        self.pac_dir = Dir.LEFT
                        self.x_spd = -2
                        self.y_spd = 0

            match self.pac_dir:
                case Dir.UP:
                    self.pac_dir_img = "up"
                case Dir.DOWN:
                    self.pac_dir_img = "down"
                case Dir.RIGHT:
                    self.pac_dir_img = "right"
                case Dir.LEFT:
                    self.pac_dir_img = "left"

            match self.pac_state:
                case 0:
                    pacman_surf = pygame.image.load(f"pacman-art/pacman-{self.pac_dir_img}/1.png").convert_alpha()
                    self.pac_state = 1
                case 1:
                    pacman_surf = pygame.image.load(f"pacman-art/pacman-{self.pac_dir_img}/2.png").convert_alpha()
                    self.pac_state = 2
                case 2:
                    pacman_surf = pygame.image.load(f"pacman-art/pacman-{self.pac_dir_img}/3.png").convert_alpha()
                    self.pac_state = 0

            pacman_rect = pacman_surf.get_rect(center=(0, 0))

            self.screen.fill("#003049")
            anchor = (600, 150)
            tile = 32
            y = 0
            for row in grid:
                x = 0
                for cell in row:
                    if cell[3] == "1":  # North
                        pygame.draw.line(
                            self.screen,
                            "white",
                            (anchor[0] + x * tile, anchor[1] + y * tile),
                            (anchor[0] + x * tile + tile, anchor[1] + y * tile),
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
                    if cell[1] == "1":  # South
                        pygame.draw.line(
                            self.screen,
                            "white",
                            (anchor[0] + x * tile, anchor[1] + y * tile + tile),
                            (anchor[0] + x * tile + tile,
                             anchor[1] + y * tile + tile),
                            2
                        )
                    if cell[0] == "1":  # West
                        pygame.draw.line(
                            self.screen,
                            "white",
                            (anchor[0] + x * tile, anchor[1] + y * tile),
                            (anchor[0] + x * tile, anchor[1] + y * tile + tile),
                            2
                        )
                    x += 1
                y += 1
            self.x_pac += self.x_spd
            self.y_pac += self.y_spd
            pacman_rect.topleft = (anchor[0] + self.x_pac, anchor[1] + self.y_pac)
            self.screen.blit(pacman_surf, pacman_rect)
            clock.tick(60)
            pygame.display.flip()








def main_screen():

    game = Game()
    while True:
        game.level()
        pygame.display.flip()



if __name__ == "__main__":
    main_screen()
