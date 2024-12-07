import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import random
from matrix import matrix
import time

class gui:
    def __init__(self):
        self.mat = matrix()
        self.matrix = self.mat.matrix
        self.X_score = 0
        self.O_score = 0
        
        self.turn = self.set_turn()
        self.window = tk.Tk()
        
        self.window.title("Tic Tac Toe Game")
        self.window.geometry("400x640")
        self.window.resizable(False, False)
        self.window.configure(bg="#BEB7BE")
        
        image = Image.open(r"assets/logo3.png")
        image = image.resize((300, 200), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        
        image_label = tk.Label(self.window, image=self.photo, bd=0)
        image_label.pack()
        image_label.place(x=50, y=20)
        
        label_font = font.Font(family="Helvetica", size=12, weight="bold")

        self.turn_label = tk.Label(self.window, text="", font=label_font, fg="#4A4A4A", bg="#FFDD8D")
        self.turn_label.place(x=170, y=225)
        self.set_turn_text()
        
        self.X_score_label = tk.Label(self.window, text=f"X-Score : {self.X_score}", font=label_font, fg="#4A4A4A", bg="#FFDD8D")
        self.X_score_label.place(x=80, y=550)
        
        self.O_score_label = tk.Label(self.window, text=f"O-Score : {self.O_score}", font=label_font, fg="#4A4A4A", bg="#FFDD8D")
        self.O_score_label.place(x=230, y=550)
        
        self.set_score()
        
        button_width = (330 - 80) / 3
        button_height = (480 - 200) / 3

        bold_font = font.Font(family="Helvetica", size=10, weight="bold")

        self.start_game = tk.Button(self.window, text="New Game", fg="white", font=bold_font, command=self.start_new)
        self.start_game.place(x=110, y=590, width=80, height=30)
        self.start_game.configure(background="#7C4DFF", activebackground="#5E29B0", relief="flat")

        self.reset_button = tk.Button(self.window, text="Reset", fg="white", font=bold_font, command=self.reset)
        self.reset_button.place(x=200, y=590, width=80, height=30)
        self.reset_button.configure(background="#7C4DFF", activebackground="#5E29B0", relief="flat")
        
        X_O_font = font.Font(family="Helvetica", size=26, weight="bold")
        self.buttons = []
        for row in range(3):
            self.buttons.append([])
            for col in range(3):    
                x = 80 + col * button_width
                y = 170 + row * button_height + 90  # Adjusted Y value to push grid down by 90px
                button = tk.Button(self.window, text=f"", command=lambda row=row, col=col: self.set_value(row, col), font=X_O_font)
                
                # Adding hover effects
                button.bind("<Enter>", lambda event, btn=button: btn.config(bg="#C0C0C0"))
                button.bind("<Leave>", lambda event, btn=button: btn.config(bg="#F0F0F0"))
                
                self.buttons[row].append(button)
                button.place(x=x, y=y, width=button_width, height=button_height)

        self.window.geometry("400x640")
        self.window.resizable(False, False)

    def set_value(self, row, col):
        if self.matrix[row][col] is None:
            if self.turn == "X":
                self.matrix[row][col] = 1
                self.buttons[row][col].config(text="X", fg="#7C4DFF")
                self.turn = "O"
                self.set_turn_text()
            elif self.turn == "O":
                self.matrix[row][col] = 0
                self.buttons[row][col].config(text="O", fg="#FF7043")
                self.turn = "X"
                self.set_turn_text()

        if self.mat.check_win() == 1:
            self.set_winner("X")
            self.mat.set_neg_one()
            return
        elif self.mat.check_win() == 0:
            self.set_winner("O")
            self.mat.set_neg_one()
            return
        
        if self.check_draw():
            self.set_draw()
        
        self.mat.print()

    def clear_buttons(self):
        for x in range(3):
            for y in range(3):
                self.buttons[x][y].config(text="")

    def run(self):
        self.window.mainloop()
    
    def reset(self):
        self.X_score = 0
        self.O_score = 0
        self.start_new()
    
    def set_turn(self):
        return random.choice(["X", "O"])
    
    def set_turn_text(self):
        if self.turn == "X":
            self.turn_label.config(text="X - Turn", fg="#4A4A4A", bg="#FFDD8D")
        elif self.turn == "O":
            self.turn_label.config(text="O - Turn", fg="#4A4A4A", bg="#FFDD8D")
    
    def set_score(self):
        self.X_score_label.config(text=f"X-Score : {self.X_score}")
        self.O_score_label.config(text=f"O-Score : {self.O_score}")
    
    def add_X(self):
        self.X_score += 1
    
    def add_O(self):
        self.O_score += 1
    
    def set_winner(self, text):
        if not self.check_draw():
            self.turn_label.config(text=f"{text} Wins", fg="#4A4A4A", bg="#FFDD8D")
            if text == "X":
                self.add_X()
            elif text == "O":
                self.add_O()
            self.set_score()
        else:
            self.set_draw()
    
    def start_new(self):
        self.set_score()
        del self.mat
        self.mat = matrix()
        self.matrix = self.mat.matrix
        self.set_turn_text()
        self.turn = self.set_turn()
        self.set_turn_text()
        self.clear_buttons()

    def set_draw(self):
        self.turn_label.config(text="Draw", fg="#4A4A4A", bg="#FFDD8D")
    
    def check_draw(self):
        return self.mat.check_draw()
