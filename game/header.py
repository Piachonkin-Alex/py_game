import pygame
import random


class Barrier:
    def __init__(self, x, y, width, movement, img):
        self.x = x
        self.y = y
        self.width = width
        self.movement = movement
        self.image = img

    def move(self, our_display, display_width):
        if self.x >= -self.width:
            our_display.blit(self.image, (self.x, self.y))
            self.x -= self.movement
            return True
        else:
            return False

    def remove_right(self, new_x, new_y, new_width, new_img):
        self.x = new_x
        self.y = new_y
        self.width = new_width
        self.image = new_img


barrier_images = []
barrier_images.append(pygame.image.load('barrier0.png'))
barrier_images.append(pygame.image.load('barrier1.png'))
barrier_images.append(pygame.image.load('barrier2.png'))
barrier_images_size = [[37, 618], [69, 657], [40, 628]]


def create_barriers(barrier_list, display_width):
    dist = [100, 500, 900]
    for i in range(3):
        choice = random.randrange(0, 3)
        img = barrier_images[choice]
        width = barrier_images_size[choice][0]
        height = barrier_images_size[choice][1]
        barrier_list.append(Barrier(display_width + dist[i], height, width, 5.2, img))


def find_distance(barrier_list, display_width):
    right_point = max(barrier_list[0].x, barrier_list[1].x, barrier_list[2].x)
    distance = 0
    if right_point < display_width:
        distance = display_width
        if distance - right_point < 250:
            distance += 300
    else:
        distance = right_point
    choice_of_dist = random.randrange(0, 12)
    if choice_of_dist < 4:
        distance += random.randrange(43, 56)
    else:
        distance += random.randrange(280, 450)
    return distance


def draw_barries(barrier_list, our_display, display_width):
    for barrier in barrier_list:
        checker = barrier.move(our_display, display_width)
        if not checker:
            distance = find_distance(barrier_list, display_width)

            choice = random.randrange(0, 3)
            img = barrier_images[choice]
            width = barrier_images_size[choice][0]
            height = barrier_images_size[choice][1]

            barrier.remove_right(distance, height, width, img)


def print_text(text: str, cord_x, cord_y, font_type, font_size, our_display):
    font = pygame.font.Font(font_type, font_size)
    text = font.render(text, True, (0, 0, 0))
    our_display.blit(text, (cord_x, cord_y))


def pause(our_display, clock):
    pause_ind = True
    while pause_ind:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        font_type = 'ofont.ru_EE-Bellflower.ttf'
        print_text('Press ENTER to continue', 300, 300, font_type, 37, our_display)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pause_ind = False
        pygame.display.update()
        clock.tick(15)


chel_images = []
chel_images.append(pygame.image.load('chel1.png'))
chel_images.append(pygame.image.load('chel2.png'))
chel_images.append(pygame.image.load('chel3.png'))

image_counter = 0


def draw_chel(our_display, cord_x, cord_y):
    global image_counter
    if image_counter == 21:
        image_counter = 0
    our_display.blit(chel_images[image_counter // 7], (cord_x, cord_y))
    image_counter += 1


def check_conflict(barrier_list, char_x, char_y, char_height, char_width):
    for barrier in barrier_list:
        if char_y + char_height >= barrier.y:
            if barrier.x <= char_x <= barrier.x + barrier.width:
                return True
            elif barrier.x <= char_x + char_width - 35 <= barrier.x + barrier.width:
                return True
    return False


def end_game(our_display, clock, score, prev_max_score):
    max_score = max(score, prev_max_score)
    end_game_ind = True
    while end_game_ind:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        font_type = 'ofont.ru_EE-Bellflower.ttf'
        first_text = 'Press ENTER to continue, esc to exit'
        print_text(first_text, 200, 300, font_type, 37, our_display)
        second_text = 'Max score is ' + str(int(max_score))
        print_text(second_text, 360, 360, font_type, 37, our_display)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False
        pygame.display.update()
        clock.tick(15)
