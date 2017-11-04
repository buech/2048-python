import sys
isPython2 = sys.version_info[0] == 2
if isPython2:
    from Tkinter import *
else:
    from tkinter import *
from logic import *
from random import *

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" , 4096:"#edc22e", 8192:"#edc22e", 16384:"#edc22e", 32768:"#edc22e", 65536:"#edc22e"}
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" , 4096:"#f9f6f2", 8192:"#f9f6f2", 16384:"#f9f6f2", 32768:"#f9f6f2", 65536:"#f9f6f2"}
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"

class GameGrid(Frame):
    def __init__(self, is_ai_game=False, useSeed = None, showGUI = True):
        self.GUImode = showGUI
        if self.GUImode:
            Frame.__init__(self)

        if useSeed:
            seed(useSeed)

        if self.GUImode:
            self.grid()
            self.master.title('2048')
            self.master.bind("<Key>", self.key_down)

        #self.gamelogic = gamelogic
        self.commands = {   KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right,
                            KEY_UP_ALT: up, KEY_DOWN_ALT: down, KEY_LEFT_ALT: left, KEY_RIGHT_ALT: right }

        self.grid_cells = []
        if self.GUImode:
            self.init_grid()
        self.init_matrix()
        if self.GUImode:
            self.update_grid_cells()

        self.endless_mode = is_ai_game # there is no "win" in AI mode
        
        if not is_ai_game:
            self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return randint(0, GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = new_game(GRID_LEN)

        self.matrix=add_two(self.matrix)
        self.matrix=add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()
        
    def key_down(self, event):
        key = repr(event.char)
        if key in self.commands:
            self.matrix,done = self.commands[repr(event.char)](self.matrix)
            if done:
                self.matrix = add_two(self.matrix)
                self.update_grid_cells()
                done=False
                if game_state(self.matrix, self.endless_mode) == 'win':
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!",bg=BACKGROUND_COLOR_CELL_EMPTY)
                if game_state(self.matrix, self.endless_mode) == 'lose':
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!",bg=BACKGROUND_COLOR_CELL_EMPTY)

    def ai_move (self, direction):
        if type(direction) == str:
            if direction.lower() == "up":
                direction = 1
            elif direction.lower() == "down":
                direction = 2
            elif direction.lower() == "right":
                direction = 3
            elif direction.lower() == "left":
                direction = 4
        if direction==1:
            self.matrix,done = self.commands[KEY_UP](self.matrix)
        elif direction==2:
            self.matrix,done = self.commands[KEY_DOWN](self.matrix)
        elif direction==3:
            self.matrix,done = self.commands[KEY_RIGHT](self.matrix)
        elif direction==4:
            self.matrix,done = self.commands[KEY_LEFT](self.matrix)
        else:
            done = False

        if done:
            self.matrix = add_two(self.matrix)
            if self.GUImode:
                self.update_grid_cells()
            # done=False
            if game_state(self.matrix, self.endless_mode)=='win':
                if self.GUImode:
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!",bg=BACKGROUND_COLOR_CELL_EMPTY)
            if game_state(self.matrix, self.endless_mode)=='lose':
                if self.GUImode:
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!",bg=BACKGROUND_COLOR_CELL_EMPTY)

        return done

    def calc_score(self):
        """ calculated the score
        Adds scores if each cell, where each cell has a score according to:
        2 -> 3
        4 -> 9
        8 -> 27
        ...
        """
        return score(self.matrix)
    
    def game_over(self):
        if game_state(self.matrix, self.endless_mode)=='not over': return False
        else: return True


    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

if __name__ == '__main__':
    gamegrid = GameGrid()
