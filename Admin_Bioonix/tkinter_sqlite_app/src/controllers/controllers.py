from models.models import ModeloTareas  # Importa el modelo que maneja las tareas y la lógica de datos.
from views.view import VistaPrincipal  # Importa la vista principal que interactúa con el usuario.

class ControladorTareas:
    """
    Clase que actúa como controlador en el patrón MVC.
    Maneja la lógica entre la vista y el modelo.
    """
    def __init__(self, root):
        """
        Inicializa el controlador, creando instancias del modelo y la vista.
        :param root: Ventana raíz de la aplicación (Tkinter).
        """
        self.modelo = ModeloTareas()  # Instancia del modelo para manejar datos.
        self.vista = VistaPrincipal(root, self)  # Instancia de la vista, pasando el controlador como referencia.
    
    def agregar_tarea(self):
        """
        Agrega una nueva tarea al modelo después de validar los datos ingresados por el usuario.
        """
        datos = self.vista.obtener_datos_entrada()  # Obtiene los datos ingresados por el usuario desde la vista.
        tarea = datos['tarea']  # Nombre de la tarea.
        tiempo = datos['tiempo']  # Tiempo estimado para la tarea.
        
        # Validación de datos: ambos campos deben estar llenos.
        if not tarea or not tiempo:
            self.vista.mostrar_error("Debes ingresar una tarea y un tiempo.")  # Muestra un mensaje de error en la vista.
            return
        
        # Validación: el tiempo debe ser un número entero.
        try:
            tiempo = int(tiempo)
        except ValueError:
            self.vista.mostrar_error("El tiempo debe ser un número.")  # Muestra un mensaje de error si el tiempo no es válido.
            return
        
        # Agrega la tarea al modelo y actualiza la vista.
        self.modelo.agregar_tarea(tarea, tiempo)
        self.actualizar_vista()
        self.vista.limpiar_entradas()  # Limpia los campos de entrada en la vista.
    
    def marcar_completado(self):
        """
        Marca una tarea como completada en el modelo.
        """
        tarea_seleccionada = self.vista.obtener_tarea_seleccionada()  # Obtiene la tarea seleccionada desde la vista.
        if not tarea_seleccionada:
            self.vista.mostrar_error("Selecciona una tarea.")  # Muestra un mensaje de error si no hay tarea seleccionada.
            return
        
        # Marca la tarea como completada en el modelo y actualiza la vista.
        if self.modelo.marcar_completado(tarea_seleccionada):
            self.actualizar_vista()
    
    def eliminar_tarea(self):
        """
        Elimina una tarea seleccionada del modelo.
        """
        tarea_seleccionada = self.vista.obtener_tarea_seleccionada()  # Obtiene la tarea seleccionada desde la vista.
        if not tarea_seleccionada:
            self.vista.mostrar_error("Selecciona una tarea.")  # Muestra un mensaje de error si no hay tarea seleccionada.
            return
        
        # Elimina la tarea del modelo y actualiza la vista.
        if self.modelo.eliminar_tarea(tarea_seleccionada):
            self.actualizar_vista()
    
    def actualizar_vista(self):
        """
        Actualiza la vista con la lista de tareas y las estadísticas actuales.
        """
        tareas = self.modelo.obtener_todas_tareas()  # Obtiene todas las tareas desde el modelo.
        estadisticas = self.modelo.obtener_estadisticas()  # Obtiene estadísticas de las tareas desde el modelo.
        self.vista.actualizar_lista_tareas(tareas)  # Actualiza la lista de tareas en la vista.
        self.vista.actualizar_progreso(estadisticas)  # Actualiza el progreso en la vista.