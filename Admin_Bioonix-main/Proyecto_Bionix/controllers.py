from models import ModeloTareas  # Asegúrate de que el archivo modelo.py contiene la clase ModeloTareas
from views import VistaPrincipal
class ControladorTareas:
    def __init__(self, root):
        self.modelo = ModeloTareas()
        self.vista = VistaPrincipal(root, self)
    
    def agregar_tarea(self):
        datos = self.vista.obtener_datos_entrada()
        tarea = datos['tarea']
        tiempo = datos['tiempo']
        
        if not tarea or not tiempo:
            self.vista.mostrar_error("Debes ingresar una tarea y un tiempo.")
            return
        
        try:
            tiempo = int(tiempo)
        except ValueError:
            self.vista.mostrar_error("El tiempo debe ser un número.")
            return
        
        self.modelo.agregar_tarea(tarea, tiempo)
        self.actualizar_vista()
        self.vista.limpiar_entradas()
    
    def marcar_completado(self):
        tarea_seleccionada = self.vista.obtener_tarea_seleccionada()
        if not tarea_seleccionada:
            self.vista.mostrar_error("Selecciona una tarea.")
            return
        
        if self.modelo.marcar_completado(tarea_seleccionada):
            self.actualizar_vista()
    
    def eliminar_tarea(self):
        tarea_seleccionada = self.vista.obtener_tarea_seleccionada()
        if not tarea_seleccionada:
            self.vista.mostrar_error("Selecciona una tarea.")
            return
        
        if self.modelo.eliminar_tarea(tarea_seleccionada):
            self.actualizar_vista()
    
    def actualizar_vista(self):
        tareas = self.modelo.obtener_todas_tareas()
        estadisticas = self.modelo.obtener_estadisticas()
        self.vista.actualizar_lista_tareas(tareas)
        self.vista.actualizar_progreso(estadisticas)