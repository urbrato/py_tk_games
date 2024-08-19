import tkinter as tk
import game_panel_engine as game

def main():
    root = tk.Tk()
    snake = game.GameBoard()
    snake.master.title('Змейка')
    root.mainloop()

if __name__ == '__main__':
    main()