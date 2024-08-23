import tkinter as tk
from tkinter import font
import tkinter.messagebox as mbox
import game_panel_engine as game
from random import randrange

class GameObject: pass

class SweeperCanvas(game.GameCanvas): pass

class GameObject:
    '''
    Игровой объект
    '''

    _INTACT_IMAGE = None
    _MINE_IMAGE = None
    _FLAG_IMAGE = None

    _FONT = None

    _COLORS = ['blue', 'green4', 'red', 'navy', 'maroon', 'turquoise', 'black', 'white']

    def __init__(self, x: int, y: int, is_mined: bool, canvas: SweeperCanvas):
        '''
        Конструктор игрового объекта

        :param x: номер клетки объекта по горизонтали
        :type x: int
        :param y: номер клетки объекта по вертикали
        :type y: int
        :param is_mined: заминирована ли клетка
        :type is_mined: bool
        :param canvas: игровая канва
        :type canvas: SweeperCanvas
        '''
        self.x = x
        self.y = y
        self.is_mined = is_mined
        self.is_open = False
        self.has_flag = False
        self._canvas = canvas

    def draw(self):
        '''
        Отрисовка объекта
        '''
        if self.has_flag:
            if GameObject._FLAG_IMAGE == None:
                GameObject._FLAG_IMAGE = tk.PhotoImage(file='sweeper_img\\flag.png')
            image = GameObject._FLAG_IMAGE
        else:
            if GameObject._INTACT_IMAGE == None:
                GameObject._INTACT_IMAGE = tk.PhotoImage(file='sweeper_img\\intact.png')
            image = GameObject._INTACT_IMAGE
        self._canvas.draw_image(self.x, self.y, image)

    def get_neighbours(self) -> list[GameObject]:
        '''
        Список соседей
        '''
        neighbours = []
        for x in range(max(0, self.x - 1), min(self._canvas._width, self.x + 2)):
            for y in range(max(0, self.y - 1), min(self._canvas._height, self.y + 2)):
                neighbours.append(self._canvas.game_field[x][y])
        return neighbours
    
    def count_mined_neighbours(self):
        '''
        Подсчёт количества заминированных соседей
        '''
        self.n_mined = len(list(filter(lambda x: x.is_mined, self.get_neighbours())))

    def open_tile(self):
        '''
        Открытие клетки
        '''
        if self.is_open or self.has_flag: return

        self.is_open = True
        if self.is_mined:
            if GameObject._MINE_IMAGE == None:
                GameObject._MINE_IMAGE = tk.PhotoImage(file='sweeper_img\\mine.png')
            self._canvas.draw_image(self.x, self.y, GameObject._MINE_IMAGE)
            self._canvas.game_lost()
        else:
            if GameObject._FONT == None:
                GameObject._FONT = font.Font(family='Courier', size=12, weight='bold')
            if self.n_mined == 0:
                text = ' '
                for cell in self.get_neighbours():
                    cell.open_tile()
            else:
                text = str(self.n_mined)
            self._canvas.draw_text(self.x, self.y, text, GameObject._COLORS[self.n_mined - 1], GameObject._FONT)
            self._canvas.n_unrevealed -= 1
            if self._canvas.n_unrevealed == self._canvas.n_mines:
                self._canvas.win()

    def toggle_flag(self):
        '''
        Пометка клетки или снятие пометки с неё
        '''
        if self.is_open: return

        self.has_flag = not self.has_flag
        self.draw()

class SweeperCanvas(game.GameCanvas):
    '''
    Игровая канва
    '''
    def init_game(self):
        '''
        Инициализация игры
        '''
        self.master.title('Сапёр')
        self.set_board_size_by_cells_size(25)
        self.set_all_cells_color('#ccc')
        self.set_all_cells_border_color('#888')
        self.create_game()

    def create_game(self):
        '''
        Инициализация новой игры
        '''
        self.n_mines = 0
        self.n_unrevealed = self._width * self._height
        mine_probability = randrange(10, 20)
        self.game_field: list[list[GameObject]]
        self.game_field = []
        for x in range(self._width):
            self.game_field.append([])
            for y in range(self._height):
                is_mined = randrange(1, 100) <= mine_probability
                if is_mined:
                    self.n_mines += 1
                gmo = GameObject(x, y, is_mined, self)
                self.game_field[x].append(gmo)
                gmo.draw()
        self.fill_mined_counts()
    
    def fill_mined_counts(self):
        '''
        Подсчёт количества заминированных соседей
        '''
        for col in self.game_field:
            for cell in col:
                cell.count_mined_neighbours()

    def game_lost(self):
        '''
        Действия при проигрыше
        '''
        if mbox.askyesno(
            'Сапёр',
            'К сожалению, сапёр подорвался на мине\nЖелаете сыграть ещё раз?'):
            self.create_game()
        else:
            self.master.destroy()

    def win(self):
        '''
        Действия при выигрыше
        '''
        if mbox.askyesno(
            'Сапёр',
            f'Успешно найдены все {self.n_mines} мин\nЖелаете сыграть ещё раз?'):
            self.create_game()
        else:
            self.master.destroy()

    def on_mouse_click(self, button: game.MouseButton, x: int, y: int):
        '''
        Обработка щелчка мышью
        '''
        match button:
            case game.MouseButton.LEFT:
                self.game_field[x][y].open_tile()
            case game.MouseButton.RIGHT:
                self.game_field[x][y].toggle_flag()

class SweeperWidget(game.GameWidget):
    '''
    Игровой виджет
    '''
    def __init__(self):
        '''
        Конструктор
        '''
        super().__init__(800, 600)

    def create_canvas(self):
        '''
        Создание канвы
        '''
        return SweeperCanvas(self)
    
def main():
    '''
    Запускатор
    '''
    root = tk.Tk()
    game = SweeperWidget()
    root.mainloop()

if __name__ == '__main__':
    main()