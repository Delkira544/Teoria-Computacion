from tkinter import Frame, Label, Text, Scrollbar, VERTICAL, RIGHT, Y, END
from lexer.lexer_engine import Lexer
from utils.file_handler import read_file_utf8

class TokenDisplay(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = Label(self, text="File Content:")
        self.label.pack()

        self.text_area = Text(self, wrap='word', height=15, width=50)
        self.text_area.pack(side='left', fill='both', expand=True)

        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.text_area.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.text_area.config(yscrollcommand=self.scrollbar.set)

        self.token_label = Label(self, text="Extracted Tokens:")
        self.token_label.pack()

        self.token_area = Text(self, wrap='word', height=10, width=50)
        self.token_area.pack(side='left', fill='both', expand=True)

        self.token_scrollbar = Scrollbar(self, orient=VERTICAL, command=self.token_area.yview)
        self.token_scrollbar.pack(side=RIGHT, fill=Y)

        self.token_area.config(yscrollcommand=self.token_scrollbar.set)

    def display_file_content(self, file_path):
        content = read_file_utf8(file_path)
        self.text_area.delete(1.0, END)
        self.text_area.insert(END, content)

        lexer = Lexer(content)
        tokens = list(lexer.tokens())
        self.token_area.delete(1.0, END)
        for token in tokens:
            self.token_area.insert(END, str(token) + '\n')