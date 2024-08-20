import tkinter as Tk
from some_math import *

class GameCanvas: pass

class GameWidget(Tk.Frame):
    '''
    Виджет игрового окна.

    Для создания своей игры унаследуйтесь от этого виджета.

    Для использования создайте окно Tk, вложите в него наследник виджета и запустите окно.
    '''
    
    def __init__(self, frame_width: int, frame_height: int):
        '''
        Конструктор виджета.

        Если игра закладывается на конкретный размер окна, в наследнике сделайте конструктор без параметров размера, а размеры передайте сюда.

        :param frame_width: ширина клиентской части окна в пикселях
        :type frame_width: int
        :param frame_height: высота клиентской части окна в пикселях
        :type frame_height: int
        '''

        super().__init__()

        # сохраняем размеры - их будет использовать канва
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # размерим и центрируем окно
        self.center_window(frame_width, frame_height)        
        
        # создаём канву и всё это добро распахиваем на всё окно
        self.canvas = self.create_canvas()
        self.pack(expand=True)

    def center_window(self, frame_width:int, frame_height:int):
        '''
        Задаёт размеры и положение окна - размеры заданные, положение по центру экрана

        :param frame_width: ширина клиентской части окна в пикселях
        :type frame_width: int
        :param frame_height: высота клиентской части окна в пикселях
        :type frame_height: int
        '''
        
        # узнаём размеры экрана
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        # вычисляем положение окна по центру
        x = (screen_width - frame_width) // 2
        y = (screen_height - frame_height) // 2
        
        # размерим и центрируем окно
        self.master.geometry(f'{frame_width}x{frame_height}+{x}+{y}')

    def create_canvas(self) -> GameCanvas:
        '''
        Создание канвы.

        При создании своей игры перекройте метод, чтобы создавалась канва нужного класса
        '''
        return GameCanvas(self)

class GameCell:
    '''
    Клетка игрового поля.
    '''
    _inner_image = None   

    def __init__(self, canvas: Tk.Canvas, 
                 left: int, top: int, size: int, 
                 outline='black', fill='white'):
        '''
        Конструктор клетки.

        :param canvas: Канва для рисования
        :type canvas: tkinter.Canvas
        :param left: левая координата клетки на канве
        :type left: int
        :param top: верхняя координата клетки на канве
        :type top: int
        :param size: размер клетки вдоль любой стороны
        :type size: int
        :param outline: цвет границы клетки
        :type outline: string
        :param fill: цвет фона клетки
        :type fill: string
        '''
        self._canvas = canvas
        self._cell_rect = canvas.create_rectangle(
            left, top, left + size, top + size,
            fill=fill, outline=outline)
        
    def set_fill_color(self, color: str):
        '''
        Установка цвета заливки клетки

        :param color: цвет фона
        :type color: str
        '''
        self._canvas.itemconfig(self._cell_rect, fill=color)

    def set_outline_color(self, color: str):
        '''
        Установка цвета границы клетки

        :param color: цвет фона
        :type color: str
        '''
        self._canvas.itemconfig(self._cell_rect, outline=color)

class GameCanvas(Tk.Canvas):
    '''
    Игровая канва.

    При создании своей игры унаследуйтесь от этого класса и переопределите нужные методы. 
    
    Пропишите создание своего класса в методе createCanvas вашего наследника GameWidget.
    '''

    _MIN_WIDTH = 3;
    _MAX_WIDTH = 100;
    _MIN_HEIGHT = 3;
    _MAX_HEIGHT = 100;
    _MIN_CELL_SIZE = 5;
    _MAX_CELL_SIZE = 200;
    
    _width: int = 3;
    _height: int = 3;
    _cellSize: int;

    _cells: list[list[GameCell]]
    
    def __init__(self, widget: GameWidget):
        super().__init__(
            width=widget.frame_width,
            height=widget.frame_height
        )
        
        self._padx = self._pady = 1
        self._frame_width = widget.frame_width - self._padx * 2
        self._frame_height = widget.frame_height - self._pady * 2
        
        self.init_game()
        self.pack()

    def init_game(self):
        '''
        Переопределите этот метод для инициализации игрового мира
        '''
        pass

    def set_board_size_by_cells_count(self, nx: int, ny: int):
        '''
        Установка размера игрового поля по количеству клеток

        :param nx: количество клеток по горизонтали
        :type nx: int
        :param ny: количество клеток по вертикали
        :type ny: int
        '''        
        self._width = clamp(nx, self._MIN_WIDTH, self._MAX_WIDTH)
        self._height = clamp(ny, self._MIN_HEIGHT, self._MAX_HEIGHT)
        self._cellSize = min(
            self._frame_width // self._width, 
            self._frame_height // self._height)
        self.__create_cells()

    def set_board_size_by_cells_size(self, cell_size: int):
        '''
        Установка размера игрового поля по размеру клетки

        :param cell_size: размер клетки
        :type cell_size: int
        '''
        self._cellSize = clamp(cell_size, 
            self._MIN_CELL_SIZE, 
            self._MAX_CELL_SIZE)
        self._width = self._frame_width // self._cellSize
        self._height = self._frame_height // self._cellSize
        self.__create_cells()

    def set_cell_color(self, x: int, y: int, color: str):
        '''
        Установка цвета заливки клетки

        :param x: номер клетки по горизонтали
        :type x: int
        :param y: номер клетки по вертикали
        :type y: int
        :param color: цвет фона
        :type color: str
        '''
        self._cells[x][y].set_fill_color(color)

    def set_all_cells_color(self, color: str):
        '''
        Установка цвета заливки всем клеткам

        :param color: цвет фона
        :type color: str
        '''
        for col in self._cells:
            for cell in col:
                cell.set_fill_color(color)

    def set_cell_border_color(self, x: int, y: int, color: str):
        '''
        Установка цвета границы клетки

        :param x: номер клетки по горизонтали
        :type x: int
        :param y: номер клетки по вертикали
        :type y: int
        :param color: цвет фона
        :type color: str
        '''
        self._cells[x][y].set_outline_color(color)

    def set_all_cells_border_color(self, color: str):
        '''
        Установка цвета границы всем клеткам

        :param color: цвет фона
        :type color: str
        '''
        for col in self._cells:
            for cell in col:
                cell.set_outline_color(color)

    def __create_cells(self):
        '''
        Создание клеток
        '''
        board_left = (self._frame_width - self._cellSize * self._width) // 2 + self._padx
        board_top = (self._frame_height - self._cellSize * self._height) // 2 + self._pady

        self._cells = []
        for i in range(self._width):
            self._cells.append([])
            for j in range(self._height):
                self._cells[i].append(
                    GameCell(self, 
                             board_left + i * self._cellSize,
                             board_top + j * self._cellSize,
                             self._cellSize))