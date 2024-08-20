import tkinter as tk
import game_panel_engine as game

class GameObject:
    '''
    Игровой объект
    '''
    def __init__(self, x: int, y: int):
        '''
        Конструктор игрового объекта

        :param x: номер клетки объекта по горизонтали
        :type x: int
        :param y: номер клетки объекта по вертикали
        :type y: int
        '''
        self.x = x
        self.y = y

class Apple(GameObject):
    '''
    Объект яблоко
    '''
    _APPLE_IMAGE = None

    def __init__(self, x: int, y: int):
        '''
        Конструктор игрового объекта

        :param x: номер клетки объекта по горизонтали
        :type x: int
        :param y: номер клетки объекта по вертикали
        :type y: int
        '''
        super().__init__(x, y)

    def draw(self, canvas: game.GameCanvas):
        '''
        Отображение яблока на канве

        :param canvas: канва для отображения в клетке
        :type canvas: game.GameCanvas
        '''
        if Apple._APPLE_IMAGE == None:
            Apple._APPLE_IMAGE = tk.PhotoImage(file='snake_img\\apple.png')

        canvas.draw_image(self.x, self.y, Apple._APPLE_IMAGE)

class SnakeCanvas(game.GameCanvas):
    '''
    Игровая канва (основной класс игры)
    '''
    def init_game(self):
        '''
        Первоначальная настройка игры
        '''
        self.master.title('Змейка')
        self.set_board_size_by_cells_size(20)
        self.create_game()

    def create_game(self):
        '''
        Настройка параметров игры
        '''
        self.create_board()

    def create_board(self):
        '''
        Настройка игрового поля
        '''
        self.set_all_cells_color('beige')

class SnakeWidget(game.GameWidget):
    '''
    Виджет игры
    '''
    def __init__(self):
        '''
        Конструктор виджета
        '''
        super().__init__(800, 600)

    def create_canvas(self):
        '''
        Создание нужной канвы
        '''
        return SnakeCanvas(self)

def main():
    '''
    Окно игры
    '''
    root = tk.Tk()
    snake = SnakeWidget()
    root.mainloop()

# Запускатор игры
if __name__ == '__main__':
    main()