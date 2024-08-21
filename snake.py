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

        self._is_alive = True

    def draw(self, canvas: game.GameCanvas):
        '''
        Отображение яблока на канве

        :param canvas: канва для отображения в клетке
        :type canvas: game.GameCanvas
        '''
        if Apple._APPLE_IMAGE == None:
            Apple._APPLE_IMAGE = tk.PhotoImage(file='snake_img\\apple.png')

        canvas.draw_image(self.x, self.y, Apple._APPLE_IMAGE)

class Snake:
    '''
    Змейка
    '''
    
    _HEAD_IMAGE = None
    _DEAD_IMAGE = None
    _BODY_IMAGE = None

    def __init__(self, x: int, y: int):
        '''
        Конструктор змейки.

        Создаёт список сегментов тела.
        Тело расположено по горизонтали головой влево.

        :param x: горизонтальная координата головы
        :type x: int
        :param y: вертикальная координата головы
        :type y: int
        '''
        self._snakeParts = [
            GameObject(x, y), 
            GameObject(x + 1, y),
            GameObject(x + 2, y)]
        
        self._is_alive = True
        
    def draw(self, canvas: game.GameCanvas):
        '''
        Отображение змейки на канве

        :param canvas: канва для отображения
        :type canvas: game.GameCanvas
        '''
        if Snake._HEAD_IMAGE == None:
            Snake._HEAD_IMAGE = tk.PhotoImage(file='snake_img\\head.png')

        if Snake._BODY_IMAGE == None:
            Snake._BODY_IMAGE = tk.PhotoImage(file='snake_img\\body.png')

        if Snake._DEAD_IMAGE == None:
            Snake._DEAD_IMAGE = tk.PhotoImage(file='snake_img\\dead.png')

        canvas.draw_image(
            self._snakeParts[0].x,
            self._snakeParts[0].y,
            Snake._HEAD_IMAGE if self._is_alive else Snake._DEAD_IMAGE)
        
        for i in range(1, len(self._snakeParts)):
            canvas.draw_image(
                self._snakeParts[i].x,
                self._snakeParts[i].y,
                Snake._BODY_IMAGE)

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
        self._snake = Snake(self._width // 2, self._height // 2)

        self.set_all_cells_color('beige')
        self.draw_board()

    def draw_board(self):
        '''
        Отрисовка игрового поля
        '''
        self._snake.draw(self)

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