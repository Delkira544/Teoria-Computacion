from tkinter import Tk, Button, filedialog, Text, Scrollbar, Frame
from typing import Optional

class FileSelector:
    def __init__(self, master: Tk):
        self.master = master
        self.master.title("File Selector")
        
        self.frame = Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        self.select_button = Button(self.frame, text="Select File", command=self.select_file)
        self.select_button.pack()

        self.text_area = Text(self.frame, wrap='word', height=15, width=50)
        self.text_area.pack(pady=10)

        self.scrollbar = Scrollbar(self.frame, command=self.text_area.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=self.scrollbar.set)

    def select_file(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.display_file_content(file_path)

    def display_file_content(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            self.text_area.delete(1.0, 'end')
            self.text_area.insert('end', content)