import tkinter as tk
from controllers import ControladorTareas

def main():
    root = tk.Tk()
    app = ControladorTareas(root)
    root.mainloop()
#esto es un comentario
if __name__ == "__main__":
    main()