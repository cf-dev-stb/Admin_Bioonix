import tkinter as tk  # Importa la biblioteca Tkinter para crear interfaces gráficas.
from tkinter import ttk, messagebox  # Importa widgets avanzados y cuadros de mensaje de Tkinter.

class VistaPrincipal:
    """
    Clase que representa la vista principal de la aplicación.
    Maneja la interfaz gráfica y la interacción con el usuario.
    """
    def __init__(self, root, controlador):
        """
        Inicializa la vista principal.
        :param root: Ventana raíz de la aplicación (Tkinter).
        :param controlador: Controlador que maneja la lógica de la aplicación.
        """
        self.root = root  # Ventana raíz de la aplicación.
        self.controlador = controlador  # Referencia al controlador.
        self.root.title("Administrador de Tareas por Tiempo")  # Título de la ventana.
        self.root.geometry("500x400")  # Dimensiones de la ventana.
        
        self.crear_interfaz()  # Llama al método para crear la interfaz gráfica.
    
    def crear_interfaz(self):
        """
        Crea y organiza los elementos de la interfaz gráfica.
        """
        # Frame para entrada de datos
        frame_entrada = tk.Frame(self.root)  # Contenedor para los campos de entrada.
        frame_entrada.pack(pady=10)  # Agrega un margen vertical.
        
        # Etiqueta y campo de entrada para el nombre de la tarea
        tk.Label(frame_entrada, text="Tarea:").grid(row=0, column=0, padx=5)  # Etiqueta para el campo de tarea.
        self.entrada_tarea = tk.Entry(frame_entrada, width=30)  # Campo de entrada para el nombre de la tarea.
        self.entrada_tarea.grid(row=0, column=1, padx=5)  # Posiciona el campo en la cuadrícula.
        
        # Etiqueta y campo de entrada para el tiempo estimado
        tk.Label(frame_entrada, text="Tiempo (min):").grid(row=0, column=2, padx=5)  # Etiqueta para el tiempo.
        self.entrada_tiempo = tk.Entry(frame_entrada, width=10)  # Campo de entrada para el tiempo estimado.
        self.entrada_tiempo.grid(row=0, column=3, padx=5)  # Posiciona el campo en la cuadrícula.
        
        # Botón para agregar una tarea
        btn_agregar = tk.Button(frame_entrada, text="Agregar", command=self.controlador.agregar_tarea)  # Botón para agregar tareas.
        btn_agregar.grid(row=0, column=4, padx=5)  # Posiciona el botón en la cuadrícula.
        
        # Treeview para mostrar tareas
        self.tree = ttk.Treeview(self.root, columns=("Tarea", "Tiempo", "Estado"), show="headings")  # Tabla para mostrar las tareas.
        self.tree.heading("Tarea", text="Tarea")  # Encabezado de la columna "Tarea".
        self.tree.heading("Tiempo", text="Tiempo (min)")  # Encabezado de la columna "Tiempo".
        self.tree.heading("Estado", text="Estado")  # Encabezado de la columna "Estado".
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)  # Posiciona y ajusta el tamaño de la tabla.
        
        # Barra de progreso
        self.barra_progreso = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")  # Barra de progreso horizontal.
        self.barra_progreso.pack(pady=10)  # Posiciona la barra con un margen vertical.
        
        # Frame para botones
        frame_botones = tk.Frame(self.root)  # Contenedor para los botones de acción.
        frame_botones.pack(pady=10)  # Agrega un margen vertical.
        
        # Botón para marcar una tarea como completada
        btn_completar = tk.Button(frame_botones, text="Marcar como Completado", command=self.controlador.marcar_completado)  # Botón para completar tareas.
        btn_completar.grid(row=0, column=0, padx=5)  # Posiciona el botón en la cuadrícula.
        
        # Botón para eliminar una tarea
        btn_eliminar = tk.Button(frame_botones, text="Eliminar Tarea", command=self.controlador.eliminar_tarea)  # Botón para eliminar tareas.
        btn_eliminar.grid(row=0, column=1, padx=5)  # Posiciona el botón en la cuadrícula.
        
        # Etiqueta para mostrar el tiempo total y completado
        self.etiqueta_tiempo = tk.Label(self.root, text="Tiempo total: 0 min | Completado: 0 min")  # Etiqueta para estadísticas de tiempo.
        self.etiqueta_tiempo.pack(pady=5)  # Posiciona la etiqueta con un margen vertical.
    
    def obtener_datos_entrada(self):
        """
        Obtiene los datos ingresados por el usuario en los campos de entrada.
        :return: Diccionario con los datos de la tarea y el tiempo.
        """
        return {
            'tarea': self.entrada_tarea.get(),  # Obtiene el texto del campo de tarea.
            'tiempo': self.entrada_tiempo.get()  # Obtiene el texto del campo de tiempo.
        }
    
    def limpiar_entradas(self):
        """
        Limpia los campos de entrada de la interfaz.
        """
        self.entrada_tarea.delete(0, tk.END)  # Borra el contenido del campo de tarea.
        self.entrada_tiempo.delete(0, tk.END)  # Borra el contenido del campo de tiempo.
    
    def mostrar_error(self, mensaje):
        """
        Muestra un cuadro de mensaje de error.
        :param mensaje: Mensaje de error a mostrar.
        """
        messagebox.showerror("Error", mensaje)  # Muestra un cuadro de error con el mensaje proporcionado.
    
    def actualizar_lista_tareas(self, tareas):
        """
        Actualiza la tabla de tareas con la lista proporcionada.
        :param tareas: Lista de tareas a mostrar.
        """
        self.tree.delete(*self.tree.get_children())  # Elimina todas las filas existentes en la tabla.
        for tarea in tareas:
            estado = "Completado" if tarea.completado else "Pendiente"  # Determina el estado de la tarea.
            self.tree.insert("", tk.END, values=(tarea.nombre, tarea.tiempo, estado))  # Agrega una fila a la tabla.
    
    def actualizar_progreso(self, estadisticas):
        """
        Actualiza la barra de progreso y la etiqueta de estadísticas con los datos proporcionados.
        :param estadisticas: Diccionario con estadísticas de tiempo.
        """
        self.barra_progreso["value"] = estadisticas['porcentaje_completado']  # Actualiza el valor de la barra de progreso.
        self.etiqueta_tiempo.config(
            text=f"Tiempo total: {estadisticas['tiempo_total']} min | Completado: {estadisticas['tiempo_completado']} min"  # Actualiza el texto de la etiqueta.
        )
    
    def obtener_tarea_seleccionada(self):
        """
        Obtiene el nombre de la tarea seleccionada en la tabla.
        :return: Nombre de la tarea seleccionada o None si no hay selección.
        """
        seleccionado = self.tree.focus()  # Obtiene el identificador del elemento seleccionado.
        if not seleccionado:
            return None  # Retorna None si no hay selección.
        item = self.tree.item(seleccionado)  # Obtiene los datos del elemento seleccionado.
        return item["values"][0] if item["values"] else None  # Retorna el nombre de la tarea o None si no hay datos.