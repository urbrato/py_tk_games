import tkinter as tk
import game_panel_engine as game

class SnakeCanvas(game.GameCanvas):
    def initGame(self):
        self.master.title('Змейка')

class SnakeWidget(game.GameWidget):
    def __init__(self):
        super().__init__(800, 600)

    def createCanvas(self):
        return SnakeCanvas(self)

def main():
    root = tk.Tk()
    snake = SnakeWidget()
    root.mainloop()

if __name__ == '__main__':
    main()