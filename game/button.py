import pygame
import header

indent = 10
font_type = 'ofont.ru_EE-Bellflower.ttf'


class Button:
    def __init__(self, width, height, color, active_color) -> None:
        """Button initiliazation"""
        self.width = width
        self.height = height
        self.color = color  # цвет пока не навели
        self.active_color = active_color  # цвет когда навели

    def draw_but(self, cord_x: int, cord_y: int, text: int, our_display, font_size: int, action=None) -> None:
        """draw button"""

        mouse = pygame.mouse.get_pos()  # координата мышки
        click = pygame.mouse.get_pressed()  # кликнули или нет

        if cord_x < mouse[0] < cord_x + self.width and cord_y < mouse[1] < cord_y + self.height:
            pygame.draw.rect(our_display, self.active_color, (cord_x, cord_y, self.width, self.height))
            if click[0] == 1:
                if action is not None:  # если нажали на кнопку -- выполнить функцию
                    action()

        else:
            pygame.draw.rect(our_display, self.color, (cord_x, cord_y, self.width, self.height))  # прорисовка
        header.print_text(text, cord_x + indent, cord_y + indent, font_type, font_size, our_display)
