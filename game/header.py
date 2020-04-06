import pygame
import random


# тут хотелось бы дать общий комментарий по поводу вообще работы с pygame. Минус этой штуки в том, что очень часто
# требуется работать с глобальными переменными. Поэтому некоторые функции в другой файл не переносятся.
# к примеру jump. В этом файле вы будете часто видеть, что я передаю всегда свой дисплей и его размеры, и поэтому
# часто в функции получается много исходных аргументов. Поэтому для меня было изначально ужобнее писыть все
# одном файле. Но я все-таки реализацию сложных вычислительных вешей постарался перенести сюда.

class Barrier:  # класс барьера
    def __init__(self, x, y, width, movement, img) -> None:  # инициализация по заданным координатам и размеру и img
        """Barrier initialization"""
        self.x = x
        self.y = y
        self.width = width
        self.movement = movement
        self.image = img

    def move(self, our_display) -> None:  # движение барьеров. Возвращает True, если барьер ушел за дисплей слева
        """Barrier motion"""
        if self.x >= -self.width:
            our_display.blit(self.image, (self.x, self.y))
            self.x -= self.movement
            return True
        else:
            return False

    def remove_right(self, new_x, new_y, new_width, new_img) -> None:  # мгновенное перемещение барьера вправо
        """replace barrier and change"""
        self.x = new_x
        self.y = new_y
        self.width = new_width
        self.image = new_img


barrier_images = []  # массив картинок барьеров
barrier_images.append(pygame.image.load('high.png'))
barrier_images.append(pygame.image.load('middle.png'))
barrier_images.append(pygame.image.load('wide.png'))
barrier_images_size = [[47, 608], [58, 628], [85, 645]]


def create_barriers(barrier_list, display_width) -> None:  # создание барьеров
    """Initialization of game Barriers"""
    dist = [100, 500, 900]  # начальная их координата
    for i in range(3):
        choice = random.randrange(0, 3)
        img = barrier_images[choice]
        width = barrier_images_size[choice][0]
        height = barrier_images_size[choice][1]  # сообственно создание
        barrier_list.append(Barrier(display_width + dist[i], height, width, 5.2, img))


def find_distance(barrier_list, display_width) -> int:
    # здесь производится случайный выбор доступного расстояния для крайних справа барьеров
    """calculate future distance between barriers"""
    right_point = max(barrier_list[0].x, barrier_list[1].x, barrier_list[2].x)  # координата самого правого барьера
    if right_point < display_width:  # проверка на то, что самый правый барьер находится за размером дисплеея
        distance = display_width
        if distance - right_point < 250:
            distance += 300
    else:
        distance = right_point
    choice_of_dist = random.randrange(0, 12)
    if choice_of_dist < 6:
        distance += random.randrange(43, 56)
    else:
        distance += random.randrange(280, 450)  # здесь происходит случайный выбор расстояния между барьерами
        # варианта 2: близко к друг другу, чтобы сразу перепрыгнуть 2, иои н нормальном расстоянии
    return distance


def draw_barries(barrier_list, our_display, display_width) -> None:
    # прорисовка барьеров на дисплей
    """draw barriers on display"""
    for barrier in barrier_list:
        checker = barrier.move(our_display)
        if not checker:  # если барьер ушел из дисплея слева, мы его перемещаем вправо согласно подсчету предыдущей ф-и
            distance = find_distance(barrier_list, display_width)

            choice = random.randrange(0, 3)
            img = barrier_images[choice]
            width = barrier_images_size[choice][0]
            height = barrier_images_size[choice][1]  # случайный выбор новго вида барьера

            barrier.remove_right(distance, height, width, img)  # перемещение


def print_text(text: str, cord_x, cord_y, font_type, font_size, our_display) -> None:  # ечать текста на дисплее
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


chel_images = []  # а тут длина строки по pep-8 не дает избежать варнинга(
chel_images.append(pygame.image.load('chel1.png'))
chel_images.append(pygame.image.load('chel2.png'))  # загрузка картинок для анимации персонажа
chel_images.append(pygame.image.load('chel3.png'))

image_counter = 0  # cчетчик смены картинки в анимации


def draw_char(our_display, cord_x, cord_y) -> None:
    """drawing character"""
    # прописовка персонажа на дисплее
    global image_counter
    if image_counter == 18:
        image_counter = 0
    our_display.blit(chel_images[image_counter // 6], (cord_x, cord_y))
    image_counter += 1


def check_conflict(barrier_list, char_x, char_y, char_height, char_width) -> bool:
    # проверка, врезались мы или нет. тут чистая математика +- некоторые константы,
    # так как мы управлчем не прямоугольниками
    """check crash"""
    for barrier in barrier_list:
        if char_y + char_height >= barrier.y:
            if barrier.x <= char_x + 5 <= barrier.x + barrier.width:
                return True
            elif barrier.x <= char_x + char_width - 60 <= barrier.x + barrier.width:
                return True
    return False


def end_game(our_display, clock, score, prev_max_score) -> None:
    # завершение игры.
    """end game screen"""
    max_score = max(score, prev_max_score)
    end_game_ind = True

    while end_game_ind:
        for event in pygame.event.get():  # нажали крестик -- вышли
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        font_type = 'ofont.ru_EE-Bellflower.ttf'  # шрифт
        first_text = 'Press ENTER to continue, esc to exit'  # надпись при прогрыше
        print_text(first_text, 200, 300, font_type, 37, our_display)  # ее вывод на экран
        second_text = 'Max score is ' + str(int(max_score))  # вывод макс. счета, полученного после открытия игры
        print_text(second_text, 360, 360, font_type, 37, our_display)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # нажали ENTER -- начали сначала
            return True
        if keys[pygame.K_ESCAPE]:  # нажали ESCAPE -- вышли из игры
            return False
        pygame.display.update()  # обновление дисплея
        clock.tick(15)
