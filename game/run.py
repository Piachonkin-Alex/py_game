import random
import pygame
import header

pygame.init()

clock = pygame.time.Clock()

display_width = 1024
display_height = 768

our_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Subway Surf 2D')

char_width = 70
char_height = 110

char_x = 3 * display_width // 10
char_y = display_height - 60 - char_height

do_jump = False
jump_count = 35


def run_game():
    global do_jump
    game = True
    barrier_list = []
    create_barriers(barrier_list)
    background = pygame.image.load(r'/home/sanches/github/py_game/game/background.png').convert()
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            do_jump = True
        if do_jump:
            jump()
        our_display.blit(background, (0, 0))
        draw_barries(barrier_list)
        pygame.draw.rect(our_display, (211, 214, 22), (char_x, char_y, char_width, char_height))
        pygame.display.update()
        clock.tick(120)


def create_barriers(barrier_list):
    barrier_list.append(header.Barrier(display_width + 25, display_height - 140, 25, 80, 5.3))
    barrier_list.append(header.Barrier(display_width + 400, display_height - 120, 30, 60, 5.3))
    barrier_list.append(header.Barrier(display_width + 840, display_height - 110, 35, 50, 5.3))
    barrier_list.append(header.Barrier(display_width + 1280, display_height - 150, 20, 90, 5.3))


def draw_barries(barrier_list):
    for barrier in barrier_list:
        checker = barrier.move(our_display, display_width)
        if not checker:
            distance = find_distance(barrier_list)
            barrier.x = distance


def find_distance(barrier_list):
    right_point = max(barrier_list[0].x, barrier_list[1].x, barrier_list[2].x, barrier_list[0].x)
    distance = 0
    if right_point < display_width:
        distance = display_width
        if distance - right_point < 150:
            distance += 320
    else:
        distance = right_point
    choice_of_dist = random.randrange(0, 12)
    if choice_of_dist < 2:
        distance += random.randrange(5, 10)
    else:
        distance += random.randrange(400, 500)
    return distance


def jump():
    global jump_count, do_jump, char_y
    if jump_count >= -35:
        char_y -= jump_count / 1.5
        jump_count -= 1
    else:
        jump_count = 35
        do_jump = False


run_game()
