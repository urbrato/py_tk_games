import tkinter as tk
import game_panel_engine as game
from random import random, randint

class Game2048Canvas(game.GameCanvas):
    '''
    Игровая канва
    '''
    def init_game(self):
        '''
        Инициализация игры
        '''
        self.master.title('2048')
        self.set_board_size_by_cells_count(4, 4)
        self.create_game()
        self.draw_board()

    def create_game(self):
        '''
        Начало новой игры
        '''
        self.game_field = [[0] * 4] * 4
        self.create_tile()
        self.create_tile()
    
    def draw_board(self):
        '''
        Первоначальная отрисовка доски
        '''
        self.set_all_cells_color('beige')

    def create_tile(self):
        '''
        Создание новой плитки
        '''
        while True:
            x = randint(0, 3)
            y = randint(0, 3)
            
            if self.game_field[x][y] == 0:
                if random() < 0.9:
                    self.game_field[x][y] = 2
                else:
                    self.game_field[x][y] = 4
                break

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