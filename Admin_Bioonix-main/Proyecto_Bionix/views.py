import tkinter as tk
from tkinter import ttk, messagebox

class VistaPrincipal:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Administrador de Tareas por Tiempo")
        self.root.geometry("500x400")
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame para entrada de datos
        frame_entrada = tk.Frame(self.root)
        frame_entrada.pack(pady=10)
        
        tk.Label(frame_entrada, text="Tarea:").grid(row=0, column=0, padx=5)
        self.entrada_tarea = tk.Entry(frame_entrada, width=30)
        self.entrada_tarea.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_entrada, text="Tiempo (min):").grid(row=0, column=2, padx=5)
        self.entrada_tiempo = tk.Entry(frame_entrada, width=10)
        self.entrada_tiempo.grid(row=0, column=3, padx=5)
        
        btn_agregar = tk.Button(frame_entrada, text="Agregar", command=self.controlador.agregar_tarea)
        btn_agregar.grid(row=0, column=4, padx=5)
        
        # Treeview para mostrar tareas
        self.tree = ttk.Treeview(self.root, columns=("Tarea", "Tiempo", "Estado"), show="headings")
        self.tree.heading("Tarea", text="Tarea")
        self.tree.heading("Tiempo", text="Tiempo (min)")
        self.tree.heading("Estado", text="Estado")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Barra de progreso
        self.barra_progreso = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.barra_progreso.pack(pady=10)
        
        # Frame para botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        
        btn_completar = tk.Button(frame_botones, text="Marcar como Completado", command=self.controlador.marcar_completado)
        btn_completar.grid(row=0, column=0, padx=5)
        
        btn_eliminar = tk.Button(frame_botones, text="Eliminar Tarea", command=self.controlador.eliminar_tarea)
        btn_eliminar.grid(row=0, column=1, padx=5)
        
        # Etiqueta de tiempo total
        self.etiqueta_tiempo = tk.Label(self.root, text="Tiempo total: 0 min | Completado: 0 min")
        self.etiqueta_tiempo.pack(pady=5)
    
    def obtener_datos_entrada(self):
        return {
            'tarea': self.entrada_tarea.get(),
            'tiempo': self.entrada_tiempo.get()
        }
    
    def limpiar_entradas(self):
        self.entrada_tarea.delete(0, tk.END)
        self.entrada_tiempo.delete(0, tk.END)
    
    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)
    
    def actualizar_lista_tareas(self, tareas):
        self.tree.delete(*self.tree.get_children())
        for tarea in tareas:
            estado = "Completado" if tarea.completado else "Pendiente"
            self.tree.insert("", tk.END, values=(tarea.nombre, tarea.tiempo, estado))
    
    def actualizar_progreso(self, estadisticas):
        self.barra_progreso["value"] = estadisticas['porcentaje_completado']
        self.etiqueta_tiempo.config(
            text=f"Tiempo total: {estadisticas['tiempo_total']} min | Completado: {estadisticas['tiempo_completado']} min"
        )
    
    def obtener_tarea_seleccionada(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            return None
        item = self.tree.item(seleccionado)
        return item["values"][0] if item["values"] else None