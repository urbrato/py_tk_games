import tkinter as tk
import tkinter.font as font
import game_panel_engine as game
from random import random, randint

class Game2048Canvas(game.GameCanvas):
    '''
    Игровая канва
    '''
    
    SIDE_LEN = 4

    def init_game(self):
        '''
        Инициализация игры
        '''
        self.master.title('2048')
        self.set_board_size_by_cells_count(Game2048Canvas.SIDE_LEN, Game2048Canvas.SIDE_LEN)
        self.colors = {
            0: 'beige', 
            2: 'pink',
            4: 'purple1',
            8: 'RoyalBlue1',
            16: 'turquoise',
            32: 'PaleGreen4',
            64: 'green2',
            128: 'orange',
            256: 'salmon',
            512: 'red2',
            1024: 'maroon1',
            2048: 'gold'}
        self.font = font.Font(family='Courier New', size=48, weight='bold')
        self.create_game()
        self.draw_board()

    def create_game(self):
        '''
        Начало новой игры
        '''
        self.game_field = []
        for i in range(Game2048Canvas.SIDE_LEN):
            self.game_field.append([])
            for j in range(Game2048Canvas.SIDE_LEN):
                self.game_field[i].append(0)
        self.create_tile()
        self.create_tile()
    
    def draw_board(self):
        '''
        Отрисовка доски
        '''
        for x in range(Game2048Canvas.SIDE_LEN):
            for y in range(Game2048Canvas.SIDE_LEN):
                self.draw_tile(x, y)

    def create_tile(self):
        '''
        Создание новой плитки
        '''
        while True:
            x = randint(0, Game2048Canvas.SIDE_LEN - 1)
            y = randint(0, Game2048Canvas.SIDE_LEN - 1)
            
            if self.game_field[x][y] == 0:
                if random() < 0.9:
                    self.game_field[x][y] = 2
                else:
                    self.game_field[x][y] = 4
                break

    def draw_tile(self, x: int, y: int):
        '''
        Отрисовка плитки

        :param x: горизонтальный индекс плитки
        :type x: int
        :param y: вертикальный индекс плитки
        :type y: int
        '''
        self.set_cell_color(x, y, self.colors[self.game_field[x][y]])
        self.draw_text(x, y, str(self.game_field[x][y]) if self.game_field[x][y] > 0 else ' ', 'black', self.font)

    def compress_list(self, lst: list[int]) -> bool:
        '''
        Сжатие списка

        Все нули в списке оттаскивает к концу

        Если удалось что-то изменить в списке, возвращает True, иначе False

        :param lst: список
        :type lst: list[int]
        '''
        result = False
        for i in range(Game2048Canvas.SIDE_LEN - 2, -1, -1):
            if lst[i] == 0:
                for j in range(i, Game2048Canvas.SIDE_LEN - 1):
                    if lst[j + 1] > 0:
                        result = True
                        lst[j], lst[j + 1] = lst[j + 1], lst[j]
        return result
    
    def merge_list(self, lst: list[int]) -> bool:
        '''
        Соединение пар одинаковых ненулевых элементов

        Если удалось что-то соединить, возвращает True, иначе False

        :param lst: список
        :type lst: list[int]
        '''
        result = False
        for i in range(Game2048Canvas.SIDE_LEN - 1):
            if lst[i] > 0 and lst[i] == lst[i + 1]:
                lst[i] *= 2
                lst[i + 1] = 0
                result = True
        return result
    
    def move_left(self): 
        '''
        Сдвиг влево
        '''
        self.game_field = list(map(
            lambda x: list(x), 
            zip(*self.game_field)))
        self.move_up()
        self.game_field = list(map(
            lambda x: list(x), 
            zip(*self.game_field)))

    def move_right(self): 
        '''
        Сдвиг вправо
        '''
        self.game_field = list(map(
            lambda x: list(x), 
            zip(*self.game_field)))
        self.move_down()
        self.game_field = list(map(
            lambda x: list(x), 
            zip(*self.game_field)))

    def move_up(self): 
        '''
        Сдвиг вверх
        '''
        changed = False

        for col in self.game_field:
            changed |= self.compress_list(col)
            changed |= self.merge_list(col)
            changed |= self.compress_list(col)

        if changed:
            self.create_tile()

    def move_down(self): 
        '''
        Сдвиг вниз
        '''
        for col in self.game_field:
            col.reverse()

        self.move_up()

        for col in self.game_field:
            col.reverse()

    def on_key_press(self, e):
        '''
        Реакция на клавиатуру
        '''
        key = e.keysym
        match key:
            case 'Left': self.move_left()
            case 'Up': self.move_up()
            case 'Right': self.move_right()
            case 'Down': self.move_down()
        self.draw_board()

class Game2048Widget(game.GameWidget):
    '''
    Игровой виджет
    '''
    def __init__(self):
        '''
        Конструктор
        '''
        super().__init__(500, 500)

    def create_canvas(self):
        '''
        Создание игровой канвы
        '''
        return Game2048Canvas(self)
    
def main():
    '''
    Запускатор
    '''
    root = tk.Tk()
    game = Game2048Widget()
    root.mainloop()

if __name__ == '__main__':
    main()