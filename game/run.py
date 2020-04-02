import pygame

pygame.init()

clock = pygame.time.Clock()

display_width = 1024
display_height = 768

our_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Subway Surf 2D')

char_width = 74
char_height = 125

char_x = 2 * display_width // 5
char_y = 535

do_jump = False


def run_game():
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            do_jump = True
        our_display.fill((128, 128, 128))
        pygame.draw.rect(our_display, (211, 214, 22), (char_x, char_y, char_width, char_height))
        pygame.display.update()
        clock.tick(80)


run_game()
