import tkinter as tk  # Importa la biblioteca Tkinter para crear la ventana principal de la aplicación.
from controllers.controllers import ControladorTareas  # Importa el controlador que maneja la lógica de la aplicación.

def main():
    """
    Función principal que inicia la aplicación.
    """
    root = tk.Tk()  # Crea la ventana raíz de la aplicación.
    app = ControladorTareas(root)  # Instancia el controlador, pasando la ventana raíz.
    root.mainloop()  # Inicia el bucle principal de la interfaz gráfica.

if __name__ == "__main__":
    main()  # Llama a la función principal si el archivo se ejecuta directamente.    git push origin comentarios-codigo