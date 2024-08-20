import tkinter as Tk

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
        self.centerWindow(frame_width, frame_height)        
        
        # создаём канву и всё это добро распахиваем на всё окно
        self.canvas = self.createCanvas()
        self.pack(expand=True)

    def centerWindow(self, frame_width:int, frame_height:int):
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

    def createCanvas(self) -> GameCanvas:
        '''
        Создание канвы.

        При создании своей игры перекройте метод, чтобы создавалась канва нужного класса
        '''
        return GameCanvas(self)

class GameCanvas(Tk.Canvas):
    '''
    Игровая канва.

    При создании своей игры унаследуйтесь от этого класса и переопределите нужные методы. 
    
    Пропишите создание своего класса в методе createCanvas вашего наследника GameWidget.
    '''
    def __init__(self, widget: GameWidget):
        super().__init__(
            width=widget.frame_width,
            height=widget.frame_height
        )
        self.initGame()
        self.pack()

    def initGame(self):
        '''
        Переопределите этот метод для инициализации игрового мира
        '''
        pass    