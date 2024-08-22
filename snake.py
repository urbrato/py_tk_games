import tkinter as tk
import tkinter.messagebox as mbox
import game_panel_engine as game
from enum import Enum
from random import randint

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

    def __init__(self, x: int, y: int, canvas: game.GameCanvas):
        '''
        Конструктор игрового объекта

        :param x: номер клетки объекта по горизонтали
        :type x: int
        :param y: номер клетки объекта по вертикали
        :type y: int
        :param canvas: канва для отображения в клетке
        :type canvas: game.GameCanvas
        '''
        super().__init__(x, y)

        self.is_alive = True
        self._canvas = canvas

    def draw(self):
        '''
        Отображение яблока на канве
        '''
        if Apple._APPLE_IMAGE == None:
            Apple._APPLE_IMAGE = tk.PhotoImage(file='snake_img\\apple.png')

        self._canvas.draw_image(self.x, self.y, Apple._APPLE_IMAGE)

    def erase(self):
        '''
        Стирает изображение яблока с экрана
        '''
        self._canvas.draw_image(self.x, self.y, None)

class Direction(Enum):
    '''
    Направление движения
    '''
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

HORIZONTAL = {Direction.LEFT, Direction.RIGHT}
VERTICAL = {Direction.UP, Direction.DOWN}

def allowables(direction):
    '''
    На какое направление можно изменить с текущего
    '''
    if direction in VERTICAL:
        return HORIZONTAL
    else:
        return VERTICAL

class SnakeCanvas(game.GameCanvas): pass

class Snake:
    '''
    Змейка
    '''
    
    _HEAD_IMAGE = None
    _DEAD_IMAGE = None
    _BODY_IMAGE = None

    def __init__(self, x: int, y: int, canvas: SnakeCanvas):
        '''
        Конструктор змейки.

        Создаёт список сегментов тела.
        Тело расположено по горизонтали головой влево.

        :param x: горизонтальная координата головы
        :type x: int
        :param y: вертикальная координата головы
        :type y: int
        :param canvas: канва для отображения
        :type canvas: game.GameCanvas
        '''
        self._snakeParts = [
            GameObject(x, y), 
            GameObject(x + 1, y),
            GameObject(x + 2, y)]
        
        self.is_alive = True
        self._direction = Direction.LEFT
        self._canvas = canvas
        
    def draw(self):
        '''
        Отображение змейки на канве
        '''
        if Snake._HEAD_IMAGE == None:
            Snake._HEAD_IMAGE = tk.PhotoImage(file='snake_img\\head.png')

        if Snake._BODY_IMAGE == None:
            Snake._BODY_IMAGE = tk.PhotoImage(file='snake_img\\body.png')

        if Snake._DEAD_IMAGE == None:
            Snake._DEAD_IMAGE = tk.PhotoImage(file='snake_img\\dead.png')

        self._canvas.draw_image(
            self._snakeParts[0].x,
            self._snakeParts[0].y,
            Snake._HEAD_IMAGE if self.is_alive else Snake._DEAD_IMAGE)
        
        for part in self._snakeParts[1:]:
            self._canvas.draw_image(part.x, part.y, Snake._BODY_IMAGE)
            
    def erase(self):
        '''
        Стирает изображение змейки с экрана
        '''
        for part in self._snakeParts:
            self._canvas.draw_image(part.x, part.y, None)
            
    def set_direction(self, direction: Direction):
        '''
        Изменение направления движения змейки
        '''
        if direction in allowables(self._direction):
            self._direction = direction

    def move(self, apple: Apple): 
        '''
        Перемещение змейки

        :param apple: яблоко
        :type apple: Apple
        '''
        head = self.create_new_head()
        
        if self.check_collision(head):
            self.is_alive = False
            self._canvas.is_game_stopped = True
        elif (head.x >= 0 and head.x < self._canvas._width and 
            head.y >= 0 and head.y < self._canvas._height):
            
            self._snakeParts.insert(0, head)

            if head.x == apple.x and head.y == apple.y:
                apple.is_alive = False
            else:
                self.remove_tail()
        else:
            self.is_alive = False
            self._canvas.is_game_stopped = True

        self.draw()

    def create_new_head(self) -> GameObject:
        '''
        Создаёт (но не добавляет) новую голову
        '''
        x = self._snakeParts[0].x
        y = self._snakeParts[0].y

        match self._direction:
            case Direction.LEFT:
                return GameObject(x - 1, y)
            case Direction.UP:
                return GameObject(x, y - 1)
            case Direction.RIGHT:
                return GameObject(x + 1, y)
            case Direction.DOWN:
                return GameObject(x, y + 1)
            
    def remove_tail(self):
        '''
        Удаляет хвост
        '''
        tail = self._snakeParts[-1]
        self._canvas.draw_image(tail.x, tail.y, None)
        self._snakeParts.remove(tail)

    def check_collision(self, object: GameObject) -> bool:
        '''
        Проверка на столкновение

        Проверяет, что переданный объект не совпадает 
        ни с одним сегментом змейки

        :param object: объект, который проверяется 
        на столкновение
        :type object: GameObject
        '''
        return not all(part.x != object.x or part.y != object.y 
                       for part in self._snakeParts)
            
class SnakeCanvas(game.GameCanvas):
    '''
    Игровая канва (основной класс игры)
    '''

    _TURN_DELAY = 300

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
        self.is_game_stopped = False

        self._snake = Snake(self._width // 2, self._height // 2, self)
        self.create_new_apple()

        self._turn_delay = SnakeCanvas._TURN_DELAY
        self.start_timer(self._turn_delay)

        self.setup_board()

    def setup_board(self):
        '''
        Отрисовка игрового поля
        '''
        self.set_all_cells_color('beige')
        self._snake.draw()

    def create_new_apple(self):
        '''
        Создание яблока
        '''
        self._apple = Apple(
            randint(0, self._width - 1), 
            randint(0, self._height - 1),
            self)
        self._apple.draw()

    def game_over(self):
        '''
        Метод конца игры
        '''
        self.stop_timer()
        if mbox.askyesno(
            'Игра окончена', 
            f'Змейка съела {len(self._snake._snakeParts) - 3} яблок.\nЖелаете повторить игру?'):

            self._apple.erase()
            self._snake.erase()
            self.create_game()
        else:
            self.master.destroy()

    def on_timer(self, timer_step: int):
        '''
        События по таймеру
        '''
        if self.is_game_stopped:
            self.game_over()
        else:
            self._snake.move(self._apple)
            if not self._apple.is_alive:
                self.create_new_apple()

    def on_key_press(self, e):
        key = e.keysym
        match key:
            case 'Left': self._snake.set_direction(Direction.LEFT)
            case 'Up': self._snake.set_direction(Direction.UP)
            case 'Right': self._snake.set_direction(Direction.RIGHT)
            case 'Down': self._snake.set_direction(Direction.DOWN)

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