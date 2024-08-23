import tkinter as tk
import game_panel_engine as game

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

    def create_game(self):
        '''
        Начало новой игры
        '''
        self.game_field = [[0] * 4] * 4
        print(self.game_field)

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