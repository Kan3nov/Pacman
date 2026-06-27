import pygame
import sys
from enum import Enum
from mazegenerator.mazegenerator import MazeGenerator
from parser import Jsonparser
import random


class Dir(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


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
        self.score = 0

    def main_menu(self) -> None:
        """
            Draw the main menu and wait for user input.

            From this screen, the user can start the game,
            show the scoreboard, or show the controls of the game.
        """

        btn_Xstart = int(self.x_size * 0.45)
        btn_Ystart = int(self.y_size * 0.4)

        play_button = pygame.Rect(btn_Xstart, btn_Ystart, 300, 75)
        score_button = pygame.Rect(btn_Xstart, btn_Ystart + 120, 300, 75)
        cont_button = pygame.Rect(btn_Xstart, btn_Ystart + 240, 300, 75)

        pac_image = (pygame.image.load("resources/Pacman_HD.png")
                     .convert_alpha()
                     )
        pac_image_rect = pac_image.get_rect()

        red_ghost = pygame.image.load("resources/redgb.png").convert_alpha()
        blue_ghost = pygame.image.load("resources/bluegb.jpeg").convert_alpha()

        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if collidePoint(play_button, mouse):
                        for lev in range(1, 11):
                            self.pacman(lev)
                    if collidePoint(pac_image_rect, mouse):
                        for lev in range(1, 11):
                            self.pacman(lev, True)
            self.screen.fill((0, 0, 0))

            resized_redG = pygame.transform.scale(red_ghost, (175, 175))
            resized_blueG = pygame.transform.scale(blue_ghost, (175, 175))
            resized_pac = pygame.transform.scale(pac_image, (200, 200))

            pygame.draw.rect(
                self.screen,
                (self.unpressed_btn if collidePoint(play_button, mouse)
                 else self.pressed_btn),
                play_button)
            pygame.draw.rect(
                self.screen,
                (self.unpressed_btn if collidePoint(score_button, mouse)
                 else self.pressed_btn),
                score_button)
            pygame.draw.rect(
                self.screen,
                (self.unpressed_btn if collidePoint(cont_button, mouse)
                 else self.pressed_btn),
                cont_button)

            title_1 = self.title_font.render("Pac", True, "yellow")
            title_2 = self.title_font.render("an", True, "yellow")

            tit1_h, _ = title_1.get_size()

            play_text = self.btnfont.render("Start Game", True,
                                            self.white_col)
            score_text = self.btnfont.render("Score board", True,
                                             self.white_col)
            cont_text = self.btnfont.render("Controls", True,
                                            self.white_col)

            self.screen.blit(play_text, (btn_Xstart + 30, btn_Ystart + 25))
            self.screen.blit(score_text, (btn_Xstart + 30, btn_Ystart + 145))
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
            pygame.display.flip()

    def ghost_dir(self, grid: list[list[str]], anchor: tuple[int, int],
                  ghost_rect: list[pygame.Rect]) -> list[tuple[int, int]]:
        """
            Determine the direction of each ghost.

            Args:
                grid: informs which walls are open in every maze cell.
                anchor: a tuple indicating the topleft position of the maze.
                ghost_rectd: a list of ghosts' rectangles.
            Returns:
                list[tuple[int, int]]: list of ghosts' speeds
        """

        speeds = []
        for ghost in ghost_rect:
            if ghost:
                x_cell = (ghost.x - anchor[0]) // 32
                y_cell = (ghost.y - anchor[1]) // 32
                cell = grid[y_cell][x_cell]
                open_paths = []
                if cell[0] == "0":
                    open_paths.append(Dir.LEFT)
                if cell[1] == "0":
                    open_paths.append(Dir.DOWN)
                if cell[2] == "0":
                    open_paths.append(Dir.RIGHT)
                if cell[3] == "0":
                    open_paths.append(Dir.UP)
                next_path = random.choice(open_paths)
                if next_path == Dir.UP:
                    speeds.append((0, -1))
                elif next_path == Dir.DOWN:
                    speeds.append((0, 1))
                elif next_path == Dir.RIGHT:
                    speeds.append((1, 0))
                elif next_path == Dir.LEFT:
                    speeds.append((-1, 0))
            else:
                speeds.append((0, 0))
        return speeds

    def ghost(self, ghost_rect: list[pygame.Rect],
              ghost_surf: list[pygame.Surface],
              speeds: list[tuple[int, int]]) -> None:
        """
            Move all ghosts in the specified directions and display them.

            Args:
                ghost_rect: contains rectangles of all ghosts
                ghost_surf: contains surfaces of all ghosts
                speeds: contains each ghosts movement direction.
        """

        for index, ghost in enumerate(ghost_rect):
            if ghost:
                speed = speeds[index]
                x_speed, y_speed = speed
                ghost.topleft = (ghost.x + x_speed, ghost.y + y_speed)
                self.screen.blit(ghost_surf[index], ghost)

    def pacgum(self, grid: list[list[str]]) -> list[list[bool]]:
        """
            Determine the distribution of all pacgums in the maze.

            Args:
                grid: informs which walls are open in every maze cell.
            Returns:
                list[list[bool]]: informs which cells contain a pacgum.
        """

        num = self.parser.json_dict["pacgum"]
        gum_grid = []
        for x in range(15):
            gum_grid.append([])
            for y in range(15):
                gum_grid[x].append(False)

        cells = []
        # Deteremine all cells that can accommodate pacgums.
        for x in range(15):
            for y in range(15):
                if (x == 0 and y == 14):
                    gum_grid[y][x] = True
                    continue
                elif (x == 0 and y == 0):
                    gum_grid[y][x] = True
                    continue
                elif (x == 14 and y == 0):
                    gum_grid[y][x] = True
                    continue
                elif (x == 14 and y == 14):
                    gum_grid[y][x] = True
                    continue
                if grid[y][x] == "1111":
                    continue
                cells.append((x, y))

        # Pick a random set out all of valid cells to put pacgums.
        gum_pos = random.sample(cells, k=num)
        for gum in gum_pos:
            gum_grid[gum[1]][gum[0]] = True
        return gum_grid

    def draw_pacgum(self, anchor: tuple[int, int],
                    gum_grid: list[list[bool]]) -> None:
        """
            Draw all pacgums and super pacgums accross the maze.

            Args:
                anchor: a tuple indicating the topleft position of the maze.
                gum_grid: a list showing the distribution of pacgums
                    accross the maze.
        """

        pacgum_surf = (pygame.image
                       .load("pacman-art/other/dot.png").convert_alpha())
        pacgum_rect = pacgum_surf.get_rect()

        app_surf = (pygame.image
                    .load("pacman-art/other/apple.png").convert_alpha())

        for y, row in enumerate(gum_grid):
            for x, cell in enumerate(row):
                if cell:
                    pos = (anchor[0] + x * 32 + 8, anchor[1] + y * 32 + 8)
                    pacgum_rect.topleft = pos
                    if ((x == 0 and y == 0) or (x == 0 and y == 14)
                            or (x == 14 and y == 0) or (x == 14 and y == 14)):
                        self.screen.blit(app_surf, pacgum_rect)
                    else:
                        self.screen.blit(pacgum_surf, pacgum_rect)

    def gameover(self, win: bool):

        username = ""
        highlight = "white"
        no_highlight = "gray"
        key_input = False
        error_font = pygame.font.Font(None, 12)

        while True:

            self.screen.fill("blue")
            if (win):
                msg = self.btnfont.render("Congratulations!")
                msg_rect = msg.get_rect(topleft=(1960 // 2 - 100, 1080 // 2))
                self.screen.blit(msg, msg_rect)
            else:
                msg = self.btnfont.render("You lost")
                msg_rect = msg.get_rect(topleft=(1960 // 2 - 100, 1080 // 2))
                self.screen.blit(msg, msg_rect)
                score = self.btnfont.render(f"Score: {self.score}")
                score_rect = score.get_rect(topleft=(1960 // 2 - 100,
                                                    1080 // 2 - 100))
                username_surf = self.btnfont.render(username)
                username_rect = username_surf.get_rect(topleft=(1960 // 2 - 100,
                                                                1960 // 2 - 200))

            for event in pygame.event.get():
                if pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if collidePoint(username_rect, pygame.mouse.get_pos()):
                            username_surf.fill(highlight)
                            key_input = True
                        else:
                            username_surf.fill(no_highlight)
                            key_input = False
                if pygame.KEYDOWN and key_input:
                    if ((str(event.unicode).isalnum() or
                            str(event.unicode) == " ") and
                            len(username) < 10):
                        username += str(event.unicode)
                    elif event.type == pygame.K_BACKSPACE:
                        username = username[: -1]
                if (username.count(" ") == len(username)
                        and len(username) > 0):
                    error_msg = error_font.render("Usernames should " +
                                                  "contain at least one " +
                                                  "alphanumeric character")
                elif (len(username) == 10):
                    error_msg = error_font.render("Usernames shouldn't " +
                                                  "exceed 10 characters")


            self.screen.blit(score, score_rect)


    def pacman(self, lev_no: str = 1, cheat_mode: bool = False):
        """
            Draw Pacman and all ghosts and control their movement.

            Pacman's movement is determined by user keyboard input, whilst
            ghosts movement is determined randomly.

            Args:
                lev_no: Level's number from 1 to 10.
                cheat_mode: if True, the player will have special abilities.
        """

        maze = MazeGenerator()
        maze.generate()
        grid = [[dec_to_bin(y, 4) for y in x] for x in maze.maze]

        x_spd = 0
        y_spd = 0
        x_pac = 8
        y_pac = 8
        pac_state = 0
        ghost_c = 0
        pac_dir_img = None
        pac_dir = Dir.RIGHT
        speeds = []

        x = (1960 - maze._width * 32) // 2
        y = (1080 - maze._height * 32) // 2
        anchor = (x, y)
        spawn = (x + 32 * 7, y + 32 * 6)
        mov_dir = None

        ghst_1surf = (pygame.image.load("pacman-art/ghosts/blinky.png")
                      .convert_alpha()
                      )
        ghst_2surf = (pygame.image.load("pacman-art/ghosts/clyde.png")
                      .convert_alpha()
                      )
        ghst_3surf = (pygame.image.load("pacman-art/ghosts/inky.png")
                      .convert_alpha()
                      )
        ghst_4surf = (pygame.image.load("pacman-art/ghosts/pinky.png")
                      .convert_alpha()
                      )
        ghst_5surf = (pygame.image.load("pacman-art/ghosts/blue_ghost.png")
                      .convert_alpha()
                      )
        # respawn points
        ghst1_res = (anchor[0] + 8, anchor[1] + 8)
        ghst2_res = (anchor[0] + (32 * (maze._width - 1)) + 8, anchor[1] + 8)
        ghst3_res = (anchor[0] + 8, anchor[1] + 32 * (maze._height - 1) + 8)
        ghst4_res = (anchor[0] + (32 * (maze._width - 1)) + 8,
                     anchor[1] + (32 * (maze._height - 1)) + 8
                     )
        ghost_res = [ghst1_res, ghst2_res, ghst3_res, ghst4_res]

        ghst_1rect = ghst_1surf.get_rect(topleft=ghst1_res)
        ghst_2rect = ghst_2surf.get_rect(topleft=ghst2_res)
        ghst_3rect = ghst_3surf.get_rect(topleft=ghst3_res)
        ghst_4rect = ghst_4surf.get_rect(topleft=ghst4_res)

        ghost_surf = [ghst_1surf, ghst_2surf, ghst_3surf, ghst_4surf]
        ghost_rect = [ghst_1rect, ghst_2rect, ghst_3rect, ghst_4rect]
        ghost_time = [None, None, None, None]

        super_pac = False
        super_time = 0

        gum_grid = self.pacgum(grid)

        clock = pygame.time.Clock()
        while True:
            self.level(anchor, grid)
            self.draw_pacgum(anchor, gum_grid)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_4:
                        pygame.quit()
                        sys.exit()
                    # To determine the direction of pacman's movement
                    if event.key == pygame.K_UP:
                        mov_dir = Dir.UP
                    elif event.key == pygame.K_DOWN:
                        mov_dir = Dir.DOWN
                    elif event.key == pygame.K_RIGHT:
                        mov_dir = Dir.RIGHT
                    elif event.key == pygame.K_LEFT:
                        mov_dir = Dir.LEFT

            # Displays the level number
            level_txt = self.btnfont.render(f"Level {lev_no}/10", True, "white")
            level_rect = level_txt.get_rect(topleft=(0, 200))
            self.screen.blit(level_txt, level_rect)

            # Ensures that pacman doesn't move unless the corresponding
            # direction is open
            if (((spawn[0] + x_pac - anchor[0]) % 32 == 8) and
                    (spawn[1] + y_pac - anchor[1]) % 32 == 8):
                x_cell = (spawn[1] + y_pac - anchor[1]) // 32
                y_cell = (spawn[0] + x_pac - anchor[0]) // 32
                if mov_dir == Dir.LEFT and grid[x_cell][y_cell][0] == "0":
                    pac_dir = Dir.LEFT
                    x_spd = -1
                    y_spd = 0
                elif mov_dir == Dir.DOWN and grid[x_cell][y_cell][1] == "0":
                    pac_dir = Dir.DOWN
                    x_spd = 0
                    y_spd = 1
                elif mov_dir == Dir.RIGHT and grid[x_cell][y_cell][2] == "0":
                    pac_dir = Dir.RIGHT
                    x_spd = 1
                    y_spd = 0
                elif mov_dir == Dir.UP and grid[x_cell][y_cell][3] == "0":
                    pac_dir = Dir.UP
                    x_spd = 0
                    y_spd = -1

            # Determine to where Pacman's face is pointed
            match pac_dir:
                case Dir.UP:
                    pac_dir_img = "up"
                case Dir.DOWN:
                    pac_dir_img = "down"
                case Dir.RIGHT:
                    pac_dir_img = "right"
                case Dir.LEFT:
                    pac_dir_img = "left"

            # Creating Pacman's Animation
            match pac_state:
                case 0:
                    pacman_surf = (pygame.image.load
                                   (f"pacman-art/pacman-{pac_dir_img}/1.png")
                                   .convert_alpha())
                case 6:
                    pacman_surf = (pygame.image.load
                                   (f"pacman-art/pacman-{pac_dir_img}/2.png")
                                   .convert_alpha())
                case 12:
                    pacman_surf = (pygame.image.load
                                   (f"pacman-art/pacman-{pac_dir_img}/3.png")
                                   .convert_alpha())
            pac_state = (pac_state + 1) % 13
            pacman_rect = pacman_surf.get_rect()

            # Check whether or not pacman has came across a pacgum
            # or a super pacgum and increases score accordingly
            if (((spawn[0] + x_pac - anchor[0]) % 32 == 8) and
                    (spawn[1] + y_pac - anchor[1]) % 32 == 8):

                x_cell = (spawn[1] + y_pac - anchor[1]) // 32
                y_cell = (spawn[0] + x_pac - anchor[0]) // 32
                if gum_grid[x_cell][y_cell]:
                    gum_grid[x_cell][y_cell] = False
                    if ((x_cell == 0 and y_cell == 0) or
                       (x_cell == 0 and y_cell == 14)
                       or (x_cell == 14 and y_cell == 0)
                       or (x_cell == 14 and y_cell == 14)):
                        self.score += (self.parser
                                       .json_dict["points_per_super_pacgum"])

                        super_time = pygame.time.get_ticks()
                        super_pac = True
                        ghost_surf = [ghst_5surf, ghst_5surf, ghst_5surf, ghst_5surf]
                    else:
                        self.score += (self.parser
                                       .json_dict["points_per_pacgum"])

                # Prevent pacman from advancing if the path is closed
                # in the movement direction
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

            pacgum_num = 0
            for row in gum_grid:
                pacgum_num += sum(row)
            if (pacgum_num <= 0):
                break

            # Update the position of Pacman
            x_pac += x_spd
            y_pac += y_spd
            pacman_rect.topleft = (spawn[0] + x_pac,
                                   spawn[1] + y_pac)

            # Check whether time of the super state has ended.
            curr_time = pygame.time.get_ticks()
            if (curr_time - super_time) > 10000:
                super_pac = False
                ghost_surf = [ghst_1surf, ghst_2surf, ghst_3surf, ghst_4surf]

            # Upon Pacman's collision with a ghost, the score increases if
            # super state was active, if otherwise, the player loses a life.
            for index, ghost in enumerate(ghost_rect):
                if ghost:
                    if collideRect(pacman_rect, ghost):
                        if super_pac:
                            ghost_rect[index] = None
                            self.score += (self.parser
                                           .json_dict["points_per_ghost"])
                            ghost_time[index] = pygame.time.get_ticks()
                        elif not cheat_mode:
                            self.parser.json_dict["lives"] -= 1
                            if self.parser.json_dict["lives"] == 0:
                                pass
                                # game_over()
                            else:
                                x_pac = 8
                                y_pac = 8
                                mov_dir = None
                                x_spd = 0
                                y_spd = 0

            # Revert back every ghost that spent over 5 seconds
            # in the fearful state.
            for index, time in enumerate(ghost_time):
                if time:
                    if (curr_time - time) > 5000:
                        ghost_time[index] = None
                        ghost_rect[index] = (ghost_surf[index].
                                             get_rect(topleft=ghost_res[index])
                                             )
            # Changes direction of ghosts every 32 frames.
            if not (ghost_c % 32):
                speeds = self.ghost_dir(grid, anchor, ghost_rect)
            ghost_c = (ghost_c + 1) % 32

            # Display ghosts and Pacman on the screen.
            self.ghost(ghost_rect, ghost_surf, speeds)
            self.screen.blit(pacman_surf, pacman_rect)

            clock.tick(60)
            pygame.display.flip()

    def level(self, anchor: tuple[int, int], grid: list[list]) -> None:
        """
            Draw the maze represented in the grid.

            Args:
                anchor: a tuple representing the topleft position
                    of the maze.
                grid: a list of lists representing the open and closed walls.
        """
        score = self.title_font.render(str(self.score), True, "yellow")
        self.screen.fill("#003049")
        self.screen.blit(score, score.get_rect(topleft=(0, 0)))
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


def main():
    """Start the UI flow"""

    game = Game()
    game.main_menu()


if __name__ == "__main__":
    main()
