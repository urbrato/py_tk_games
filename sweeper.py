import tkinter as tk
import game_panel_engine as game

class SweeperCanvas(game.GameCanvas):
    def init_game(self):
        self.master.title('Сапёр')
        self.set_board_size_by_cells_size(25)

class SweeperWidget(game.GameWidget):
    def __init__(self):
        super().__init__(800, 600)

    def create_canvas(self):
        return SweeperCanvas(self)
    
def main():
    root = tk.Tk()
    game = SweeperWidget()
    root.mainloop()

if __name__ == '__main__':
    main()