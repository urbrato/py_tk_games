import tkinter as Tk

class GameBoard(Tk.Frame):
    def __init__(self):
        super().__init__()
        self.canvas = Game()
        self.pack()

class Game(Tk.Canvas):
    _left: int
    _top: int
    _width: int
    _height: int