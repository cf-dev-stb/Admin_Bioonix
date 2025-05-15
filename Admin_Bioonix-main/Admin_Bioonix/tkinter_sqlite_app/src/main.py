import tkinter as tk
from controllers.controllers import ControladorTareas

def main():
    root = tk.Tk()
    app = ControladorTareas(root)
    root.mainloop()

if __name__ == "__main__":
    main()