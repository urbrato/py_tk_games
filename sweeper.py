import tkinter as tk
import game_panel_engine as game

class SweeperCanvas(game.GameCanvas): pass

class GameObject:
    '''
    Игровой объект
    '''

    _INTACT_IMAGE = None

    def __init__(self, x: int, y: int, canvas: SweeperCanvas):
        '''
        Конструктор игрового объекта

        :param x: номер клетки объекта по горизонтали
        :type x: int
        :param y: номер клетки объекта по вертикали
        :type y: int
        :param canvas: игровая канва
        :type canvas: SweeperCanvas
        '''
        self.x = x
        self.y = y
        self._canvas = canvas

    def draw(self):
        '''
        Отрисовка объекта
        '''
        if self._INTACT_IMAGE == None:
            self._INTACT_IMAGE = tk.PhotoImage(file='sweeper_img\\intact.png')
        image = self._INTACT_IMAGE
        self._canvas.draw_image(self.x, self.y, image)

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
        self.set_all_cells_border_color('silver')
        self.create_game()

    def create_game(self):
        self.game_field: list[list[GameObject]]
        self.game_field = []
        for x in range(self._width):
            self.game_field.append([])
            for y in range(self._height):
                gmo = GameObject(x, y, self)
                self.game_field[x].append(gmo)
                gmo.draw()

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