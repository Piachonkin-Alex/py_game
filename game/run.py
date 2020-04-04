import random
import pygame
import header

pygame.init()

font_type = 'ofont.ru_EE-Bellflower.ttf'

clock = pygame.time.Clock()

display_width = 1024
display_height = 768

our_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Subway Surf 2D')

char_width = 111
char_height = 139

char_x = 3 * display_width // 10
char_y = display_height - 60 - char_height

do_jump = False
jump_count = 33

score = 0
max_score = 0


def jump():
    global jump_count, do_jump, char_y
    if jump_count >= -33:
        char_y -= jump_count / 1.7
        jump_count -= 1
    else:
        jump_count = 33
        do_jump = False


def count_score():
    global score
    score += 1 / 180


def run_game():
    global do_jump
    game = True
    barrier_list = []
    header.create_barriers(barrier_list, display_width)
    background = pygame.image.load(r'background.png').convert()
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            do_jump = True

        if keys[pygame.K_ESCAPE]:
            header.pause(our_display, clock)
        if do_jump:
            jump()
        count_score()
        our_display.blit(background, (0, 0))
        header.print_text('score: ' + str(int(score)), 45, 22, font_type, 35, our_display)
        header.draw_barries(barrier_list, our_display, display_width)
        header.draw_chel(our_display, char_x, char_y)
        if header.check_conflict(barrier_list, char_x, char_y, char_width, char_height):
            game = False
        pygame.display.update()
        clock.tick(70)
    return header.end_game(our_display, clock, score, max_score)


while run_game():
    if score > max_score:
        max_score = score
    do_jump = False
    jump_count = 33
    score = 0
    char_y = display_height - 60 - char_height
pygame.quit()
quit()
