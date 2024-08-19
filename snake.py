import tkinter as tk
import game_panel_engine as game

class SnakeCanvas(game.GameCanvas):
    def initGame(self):
        self.create_oval(0, 0, 800, 600)

class SnakeWidget(game.GameWidget):
    def __init__(self):
        super().__init__(800, 600)

    def createCanvas(self, frame_width, frame_height):
        return SnakeCanvas(frame_width, frame_height)

def main():
    root = tk.Tk()
    snake = SnakeWidget()
    snake.master.title('Змейка')
    root.mainloop()

if __name__ == '__main__':
    main()