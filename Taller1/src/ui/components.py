import tkinter as tk
from tkinter import ttk

class LabeledEntry(tk.Frame):
    def __init__(self, master, label, textvariable=None, **kwargs):
        super().__init__(master)
        tk.Label(self, text=label).pack(side="left", padx=5)
        self.entry = tk.Entry(self, textvariable=textvariable, **kwargs)
        self.entry.pack(side="left", fill="x", expand=True)

class LabeledCheck(tk.Frame):
    def __init__(self, master, label, variable, **kwargs):
        super().__init__(master)
        self.check = tk.Checkbutton(self, text=label, variable=variable, **kwargs)
        self.check.pack(side="left")

class LabeledButton(tk.Frame):
    def __init__(self, master, label, command, **kwargs):
        super().__init__(master)
        self.button = tk.Button(self, text=label, command=command, **kwargs)
        self.button.pack(side="left")

class ResultsTable(ttk.Treeview):
    def __init__(self, master, **kwargs):
        super().__init__(master, columns=("linea", "correo", "estado", "motivo"), show="headings", **kwargs)
        for col in ["linea", "correo", "estado", "motivo"]:
            self.heading(col, text=col.capitalize())
            self.column(col, width=120)
