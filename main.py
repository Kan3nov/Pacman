import pygame
import sys



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
def start_screen(params: dict):

    x_size = params["x_size"]
    y_size = params["y_size"]
    screen = params["screen"]
    btnfont = params["btnfont"]
    pressed_btn = params["pressed_btn"]
    unpressed_btn = params["unpressed_btn"]
    white_col = params["white_col"]
    title_font = params["title_font"]

    while True:
        btn_Xstart = int(x_size * 0.45)
        btn_Ystart = int(y_size * 0.4)
        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()

        #screen.fill("#003049")

        play_button = pygame.Rect(btn_Xstart, btn_Ystart, 300, 75)
        score_button = pygame.Rect(btn_Xstart, btn_Ystart + 120, 300, 75)
        cont_button = pygame.Rect(btn_Xstart, btn_Ystart + 240, 300, 75)
        pac_image = pygame.image.load("resources/Pacman_HD.png").convert_alpha()
        red_ghost = pygame.image.load("resources/redgb.png").convert_alpha()
        blue_ghost = pygame.image.load("resources/bluegb.jpeg").convert_alpha()

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

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #if event.type == pygame.MOUSEBUTTONDOWN:

                #if play_button.collidepoint(mouse):
                #    game()

        pygame.display.flip()


def main_screen():
    pygame.init()
    x_size = 1920
    y_size = 1080
    screen = pygame.display.set_mode((x_size, y_size))
    pygame.display.set_caption("Start Menu Example")
    pygame.Color("#003049")

    pressed_btn = (253, 216, 53)
    unpressed_btn = (251, 192, 45)
    white_col = (255, 255, 255)
    btnfont = pygame.font.SysFont("Corbel", 60)
    title_font = pygame.font.SysFont("Corbel", 200)
    params = {
        "x_size": x_size,
        "y_size": y_size,
        "screen": screen,
        "btnfont": btnfont,
        "title_font": title_font,
        "pressed_btn": pressed_btn,
        "unpressed_btn": unpressed_btn,
        "white_col": white_col
    }
    start_screen(params)


if __name__ == "__main__":
    main_screen()
