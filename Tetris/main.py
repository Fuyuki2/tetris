import pygame, sys, os
from game import Game
from colors import Colors

pygame.init()


def get_path(filename):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)


sound1_path = get_path("newagesoup_explosion09.wav")
music_path = get_path("reggaeton-x-dancehall.mp3")
font_path = get_path("akashi.ttf")

game = Game(sound1_path, music_path)

font_path = get_path("akashi.ttf")
title_font = pygame.font.Font(font_path, 30)

score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 80, 170, 60)
next_rect = pygame.Rect(320, 240, 170, 180)

# Janela do jogo
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over:
                game.game_over = False
                game.reset()

            if not game.game_over:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                elif event.key == pygame.K_DOWN:
                    game.move_down()
                    game.update_score(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()

    # Drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (360, 20))
    screen.blit(next_surface, (365, 180))

    if game.game_over:
        screen.blit(game_over_surface, (320, 450))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(
        score_value_surface,
        score_value_surface.get_rect(
            centerx=score_rect.centerx, centery=score_rect.centery
        ),
    )
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)
