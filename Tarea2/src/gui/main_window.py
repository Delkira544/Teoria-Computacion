from tkinter import Tk, Frame, Button, Text, Scrollbar, Label, filedialog
from lexer.lexer_engine import Lexer
from utils.file_handler import read_file_utf8

class MainWindow:
    def __init__(self, master: Tk):
        self.master = master
        self.master.title("Lexer GUI")
        self.master.geometry("600x400")

        self.frame = Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        self.label = Label(self.frame, text="Select a file to tokenize:")
        self.label.pack(pady=10)

        self.select_button = Button(self.frame, text="Select File", command=self.select_file)
        self.select_button.pack(pady=5)

        self.text_area = Text(self.frame, wrap="word")
        self.text_area.pack(fill="both", expand=True, padx=10, pady=10)

        self.scrollbar = Scrollbar(self.text_area)
        self.scrollbar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        self.token_label = Label(self.frame, text="Extracted Tokens:")
        self.token_label.pack(pady=10)

        self.token_area = Text(self.frame, wrap="word", height=10)
        self.token_area.pack(fill="both", expand=True, padx=10, pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Source Files", "*.src"), ("All Files", "*.*")])
        if file_path:
            self.display_file_content(file_path)
            self.display_tokens(file_path)

    def display_file_content(self, file_path: str):
        content = read_file_utf8(file_path)
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", content)

    def display_tokens(self, file_path: str):
        content = read_file_utf8(file_path)
        lexer = Lexer(content)
        self.token_area.delete(1.0, "end")
        for token in lexer.tokens():
            self.token_area.insert("end", str(token) + "\n")