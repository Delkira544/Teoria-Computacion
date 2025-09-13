# main.py (raíz)
import os, sys
SRC = os.path.join(os.path.dirname(__file__), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from ui.main_window import MainApp  # <-- NO uses main_windowold

def main():
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()
