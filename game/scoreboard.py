import header

font_type = 'ofont.ru_EE-Bellflower.ttf'
font_size = 45


class Scoreboard:
    def __init__(self, board) -> None:
        # представляет собой лист из элементов, которые являетются листами длины с именем и числом очков
        self.board = board

    def update_board(self, name, scores) -> None:
        self.board.append([scores, name])
        self.board = sorted(self.board) # храним только лучшие 10
        while len(self.board) > 10:
            self.board = self.board[1:]

    def print(self, cord_x: int, cord_y: int, step_x: int, step_y: int, our_display) -> None:
        # вывод на дисплей и опред. пробелами
        header.print_text('Name', cord_x, cord_y, font_type, font_size, our_display)
        header.print_text('Score', cord_x + step_x, cord_y, font_type, font_size, our_display)
        cord_y += step_y + 30
        for res in self.board[::-1]: # выводим обратный порядок
            header.print_text(res[1], cord_x, cord_y, font_type, font_size, our_display)
            header.print_text(str(res[0]), cord_x + step_x, cord_y, font_type, font_size, our_display)
            cord_y += step_y
