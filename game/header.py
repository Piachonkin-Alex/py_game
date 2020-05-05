import pygame
import random
import run
import scoreboard
import saving


# тут хотелось бы дать общий комментарий по поводу вообще работы с pygame. Минус этой штуки в том, что очень часто
# требуется работать с глобальными переменными.
# Поэтому некоторые функции в другой файл не переносятся.
# к примеру jump. В этом файле вы будете часто видеть,
# что я передаю всегда свой дисплей и его размеры, и поэтому
# часто в функции получается много исходных аргументов.
# Поэтому для меня было изначально удобнее писать все
# одном файле.
# Но я все-таки реализацию сложных вычислительных вещей постарался перенести сюда.


class Barrier:  # класс барьера
    def __init__(self, x, y, width, movement, img) -> None:
        # инициализация по заданным координатам и размеру и img
        """Barrier initialization"""
        self.x = x
        self.y = y
        self.width = width
        self.movement = movement
        self.image = img

    def move(self, our_display) -> None:
        # движение барьеров. Возвращает True, если барьер ушел за дисплей слева
        """Barrier motion"""
        if self.x >= -self.width:
            our_display.blit(self.image, (self.x, self.y))
            self.x -= self.movement
            return True
        else:
            return False

    def remove_right(self, new_x, new_y, new_width, new_img) -> None:
        # мгновенное перемещение барьера вправо
        """replace barrier and change"""
        self.x = new_x
        self.y = new_y
        self.width = new_width
        self.image = new_img


barrier_images = []  # массив картинок барьеров
for i in range(3):
    barrier_images.append(pygame.image.load('bar{}.png'.format(str(i))))
    # загрузка в массив. //fixed

barrier_images_size = [[47, 608], [58, 628], [85, 645]]  # размеры барьеров

speed = 5.2  # скорость движения картинки
dist = [100, 500, 900]  # начальная их координата


def create_barriers(barrier_list, display_width) -> None:  # создание барьеров
    """Initialization of game Barriers"""
    for j in range(3):
        choice = random.randrange(0, len(barrier_images))
        img = barrier_images[choice]
        width, height = barrier_images_size[choice]  # fixed
        barrier_list.append(Barrier(display_width + dist[j], height, width, speed, img))


min_good_dist_to_display = 250
near_min_dist = 43
near_max_dist = 56
far_min_dist = 280
far_max_dist = 450


def find_distance(barrier_list, display_width) -> int:
    # здесь производится случайный выбор доступного расстояния для крайних справа барьеров
    """calculate future distance between barriers"""
    right_point = max(barrier_list[0].x, barrier_list[1].x, barrier_list[2].x)
    # координата самого правого барьера
    if right_point < display_width:
        # проверка на то, что самый правый барьер находится за размером дисплея
        distance = display_width
        if distance - right_point < min_good_dist_to_display:
            distance += (min_good_dist_to_display + 50)
    else:
        distance = right_point
    choice_of_dist = random.randrange(0, 12)
    # это просто рандом, выбирающий взаимное расположение барьеров
    if choice_of_dist < 6:
        distance += random.randrange(near_min_dist, near_max_dist)
    else:
        distance += random.randrange(far_min_dist, far_max_dist)
        # здесь происходит случайный выбор расстояния между барьерами
        # варианта 2: близко к друг другу, чтобы сразу перепрыгнуть 2
        #  или на нормальном расстоянии
    return distance


def draw_barries(barrier_list, our_display, display_width) -> None:
    # прорисовка барьеров на дисплей
    """draw barriers on display"""
    for barrier in barrier_list:
        checker = barrier.move(our_display)
        if not checker:
            # если барьер ушел из дисплея слева,
            # мы его перемещаем вправо согласно подсчету предыдущей ф-и
            distance = find_distance(barrier_list, display_width)

            choice = random.randrange(0, 3)
            img = barrier_images[choice]
            width = barrier_images_size[choice][0]
            height = barrier_images_size[choice][1]  # случайный выбор новго вида барьера

            barrier.remove_right(distance, height, width, img)  # перемещение


def print_text(text: str, cord_x, cord_y, font_type, font_size, our_display) -> None:
    # печать текста на дисплее
    """print text on display"""
    font = pygame.font.Font(font_type, font_size)
    text = font.render(text, True, (0, 0, 0))
    our_display.blit(text, (cord_x, cord_y))


def pause(our_display, clock) -> None:  # пауза
    """game pause"""
    pause_ind = True
    pygame.mixer.music.pause()  # пауза в музыке

    while pause_ind:
        for event in pygame.event.get():  # нажали крестик -- вышли
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        font_type = 'ofont.ru_EE-Bellflower.ttf'  # прописовка надписи при паузе
        print_text('Press ENTER to continue', 300, 300, font_type, 37, our_display)

        keys = pygame.key.get_pressed()  # считывание нажатых клавиш
        if keys[pygame.K_RETURN]:  # нажали ENTER -- продолжили игру
            pause_ind = False
        pygame.display.update()  # обновление дисплея
        clock.tick(15)

    pygame.mixer.music.unpause()  # убираем паузу с музыки


chel_images = []  # массив картинок для анимации персонажа
for i in range(3):
    chel_images.append(pygame.image.load('chel{}.png'.format(str(i))))

image_counter = 0  # cчетчик смены картинки в анимации


def draw_char(our_display, cord_x, cord_y) -> None:
    """drawing character"""
    # прописовка персонажа на дисплее
    global image_counter
    if image_counter == 17:
        image_counter = 0
    our_display.blit(chel_images[image_counter // 6], (cord_x, cord_y))
    image_counter += 1


def check_conflict(barrier_list, char_x, char_y, char_height, char_width) -> bool:
    # проверка, врезались мы или нет. тут чистая математика +- некоторые константы,
    # так как мы управляем не прямоугольниками
    """check crash"""
    for barrier in barrier_list:
        if char_y + char_height >= barrier.y:
            if barrier.x <= char_x + 5 <= barrier.x + barrier.width:
                return True
            elif barrier.x <= char_x + char_width - 60 <= barrier.x + barrier.width:
                return True
    return False


need_input = False
text_input = ''


def end_game(disp, clock, score, prev_max, barrier_list, ch_x, ch_y, high_scr, data):
    # завершение игры.
    """end game screen"""
    global need_input, text_input
    max_score = max(score, prev_max)
    end_game_ind = True
    name = ''
    while end_game_ind:
        for event in pygame.event.get():  # нажали крестик -- вышли
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if need_input and event.type == pygame.KEYDOWN:  # если вводим имя
                if event.key == pygame.K_TAB:  # нажали таб снова -- закончили вводить имя
                    name = text_input
                    if name:  # если имя не пусто -- добавляем в таблицу
                        high_scr.update_board(name, int(score))
                        data.add_data('score', high_scr.board)
                    need_input = False
                    text_input = ''
                elif event.key == pygame.K_BACKSPACE:  # стирание через бэкспейс
                    text_input = text_input[:-1]
                else:
                    if len(text_input) < 15:  # не более 15 символов
                        text_input += event.unicode

        font_type = 'ofont.ru_EE-Bellflower.ttf'  # шрифт
        disp.blit(pygame.image.load('background.png'), (0, 0))
        for barrier in barrier_list:
            disp.blit(barrier.image, (barrier.x, barrier.y))
        disp.blit(chel_images[image_counter // 6], (ch_x, ch_y))
        if not name:
            print_text("Press Tab to enter your name:", 90, 400, font_type, 37, disp)
        first_text = 'Press ENTER to continue, esc to exit'  # надпись при прогрыше
        print_text(first_text, 200, 240, font_type, 37, disp)  # ее вывод на экран
        second_text = 'Max score is ' + str(int(max_score))
        # вывод макс. счета, полученного после открытия игры
        print_text(second_text, 360, 300, font_type, 37, disp)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # нажали ENTER -- начали сначала
            return True
        if keys[pygame.K_ESCAPE]:  # нажали ESCAPE -- вышли из игры
            return False
        if keys[pygame.K_TAB] and not name:  # нажали таб -- водим имя
            need_input = True
        print_text(text_input, 650, 400, font_type, 37, disp)
        pygame.display.update()  # обновление дисплея
        clock.tick(15)
