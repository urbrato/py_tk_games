import tkinter as Tk

class GameCanvas(Tk.Canvas):
    def __init__(self, frame_width: int, frame_height: int):
        super().__init__(
            width=frame_width,
            height=frame_height
        )
        self.initGame()
        self.pack()

    def initGame(self):
        pass

class GameWidget(Tk.Frame):
    def __init__(self, frame_width: int, frame_height: int):
        super().__init__()
        self.centerWindow(frame_width, frame_height)
        self.canvas = self.createCanvas(frame_width, frame_height)
        self.pack(expand=True)

    def centerWindow(self, frame_width:int, frame_height:int):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width - frame_width) // 2
        y = (screen_height - frame_height) // 2

        self.master.geometry(f'{frame_width}x{frame_height}+{x}+{y}')

    def createCanvas(self, frame_width, frame_height) -> GameCanvas:
        return GameCanvas(frame_width, frame_height)