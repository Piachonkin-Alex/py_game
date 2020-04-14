import random
import pygame
import header
import button
from scoreboard import *
import saving

pygame.init()

pygame.mixer.music.load('background.mp3')  # загрузка музыки

font_type = 'ofont.ru_EE-Bellflower.ttf'  # загрузка шрифта

clock = pygame.time.Clock()  # счетчик кадров и времени

display_width = 1024
display_height = 768  # размеры дисплея

our_display = pygame.display.set_mode((display_width, display_height))  # создание дисплея
pygame.display.set_caption('Subway Surf 2D')

char_width = 111
char_height = 139  # размеры героя

char_x = 3 * display_width // 10
char_y = display_height - 60 - char_height  # координата местоположения героя

do_jump = False  # индикатор прыжка
jump_count = 33  # счетчик смены координаты прыжка прыжка

score = 0  # счет
max_score = 0  # максимальный счет при запуске окна

save_data = saving.Save()
high_scores = Scoreboard(save_data.get_data('score'))  # сохраненная таблица рекордов


def jump() -> None:
    """Do jump"""
    global jump_count, do_jump, char_y
    if jump_count >= -33:  # пока счетчик не достиг -33 меняем координату героя
        char_y -= jump_count / 1.7
        jump_count -= 1
    else:
        jump_count = 33
        do_jump = False


def count_score() -> None:
    """Counting score"""
    global score  # при вызове функции немного увеличиваем счет
    score += 1 / 180


active_color = (255, 215, 0)
color = (255, 255, 0)


def show_menu() -> None:
    """Menu"""
    background = pygame.image.load('background.png')
    show_men = True

    but_start = button.Button(180, 75, color, active_color)
    but_records = button.Button(280, 75, color, active_color)  # прорисовка кнопок.
    but_end = button.Button(120, 75, color, active_color)
    while show_men:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выход из программы при нажатии крестика
                pygame.quit()
                quit()
        our_display.blit(background, (0, 0))
        but_start.draw_but(420, 200, 'Start!', our_display, 50, start_game)
        but_records.draw_but(365, 325, 'Scoreboard', our_display, 50, show_record_table)  # прорисовка кнопок
        but_end.draw_but(450, 450, 'Quit', our_display, 50, quit)
        pygame.display.update()
        clock.tick(60)


def show_record_table() -> None:
    background = pygame.image.load('background.png')
    show_record = True
    while show_record:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выход из программы при нажатии крестика
                pygame.quit()
                quit()
        our_display.blit(background, (0, 0))
        high_scores.print(80, 100, 300, 50, our_display)  # вывод таблицы рекордов
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            show_record = False
            show_menu()
        pygame.display.update()  # обновление дисплея
        clock.tick(30)


def start_game():
    global score, max_score, do_jump, jump_count, char_y
    while run_game():  # пока запускаем игру
        if score > max_score:  # меняем максимальный счет, если это надо
            max_score = score
        do_jump = False
        jump_count = 33
        score = 0
        char_y = display_height - 60 - char_height  # меняем нужные переменные на начальные условия
        save_data.add_data('score', high_scores.board)
        a = 0


def run_game() -> bool:  # цикл игры. Сама механика игры -- это цикл, который прерывается только при выходе
    """Game cycle process"""
    global do_jump
    global high_scores
    pygame.mixer.music.play(-1)  # проигрывание музыки
    background = pygame.image.load(r'background.png').convert()  # загрузка изображения фона
    game = True

    barrier_list = []
    header.create_barriers(barrier_list, display_width)  # создание препядствий
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выход из программы при нажатии крестика
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()  # считывание нажатых клавиш в данный момент

        if keys[pygame.K_SPACE]:  # нажали пробел -- прыжок
            do_jump = True

        if keys[pygame.K_ESCAPE]:  # нажали ESCAPE -- пауза
            header.pause(our_display, clock)

        if do_jump:  # прыжок, если горит индикатор прыжка
            jump()

        count_score()  # счет очков не забываем

        our_display.blit(background, (0, 0))  # заливка фона на дисплей
        header.print_text('score: ' + str(int(score)), 45, 22, font_type, 35, our_display)  # табло очков на фоне
        header.draw_barries(barrier_list, our_display, display_width)  # прорисовка барьеров
        header.draw_char(our_display, char_x, char_y)  # прорисовка персонажа

        if header.check_conflict(barrier_list, char_x, char_y, char_width, char_height):
            # проверка на то, что не врезались
            pygame.mixer.music.stop()  # остановка музыки
            game = False  # выход из цикла игры

        pygame.display.update()  # обновление дисплея
        clock.tick(70)  # частота
    return header.end_game(our_display, clock, score, max_score, barrier_list, char_x, char_y, high_scores, save_data)
    # возвращаем True или False, в зависимости от того, хотим ли еще играть


show_menu()

pygame.quit()
quit()
