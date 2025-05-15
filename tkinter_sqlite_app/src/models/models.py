class Tarea:
    """
    Clase que representa una tarea individual.
    """
    def __init__(self, nombre, tiempo):
        """
        Inicializa una tarea con su nombre, tiempo estimado y estado de completado.
        :param nombre: Nombre de la tarea.
        :param tiempo: Tiempo estimado para completar la tarea.
        """
        self.nombre = nombre  # Nombre de la tarea.
        self.tiempo = tiempo  # Tiempo estimado para la tarea.
        self.completado = False  # Estado de la tarea (False por defecto).

class ModeloTareas:
    """
    Clase que actúa como modelo en el patrón MVC.
    Maneja la lógica de datos y las operaciones relacionadas con las tareas.
    """
    def __init__(self):
        """
        Inicializa el modelo con una lista de tareas y estadísticas de tiempo.
        """
        self.tareas = []  # Lista que almacena las tareas.
        self.tiempo_total = 0  # Tiempo total de todas las tareas.
        self.tiempo_completado = 0  # Tiempo total de las tareas completadas.
    
    def agregar_tarea(self, nombre, tiempo):
        """
        Agrega una nueva tarea a la lista de tareas.
        :param nombre: Nombre de la tarea.
        :param tiempo: Tiempo estimado para completar la tarea.
        :return: La tarea creada.
        """
        tarea = Tarea(nombre, tiempo)  # Crea una nueva instancia de Tarea.
        self.tareas.append(tarea)  # Agrega la tarea a la lista.
        self.tiempo_total += tiempo  # Actualiza el tiempo total.
        return tarea
    
    def marcar_completado(self, nombre_tarea):
        """
        Marca una tarea como completada si coincide con el nombre proporcionado.
        :param nombre_tarea: Nombre de la tarea a marcar como completada.
        :return: True si la tarea fue marcada como completada, False en caso contrario.
        """
        for tarea in self.tareas:
            if tarea.nombre == nombre_tarea and not tarea.completado:
                tarea.completado = True  # Cambia el estado de la tarea a completado.
                self.tiempo_completado += tarea.tiempo  # Actualiza el tiempo completado.
                return True
        return False
    
    def eliminar_tarea(self, nombre_tarea):
        """
        Elimina una tarea de la lista si coincide con el nombre proporcionado.
        :param nombre_tarea: Nombre de la tarea a eliminar.
        :return: True si la tarea fue eliminada, False en caso contrario.
        """
        for tarea in self.tareas:
            if tarea.nombre == nombre_tarea:
                if tarea.completado:
                    self.tiempo_completado -= tarea.tiempo  # Actualiza el tiempo completado si la tarea estaba completada.
                self.tiempo_total -= tarea.tiempo  # Actualiza el tiempo total.
                self.tareas.remove(tarea)  # Elimina la tarea de la lista.
                return True
        return False
    
    def obtener_todas_tareas(self):
        """
        Devuelve la lista completa de tareas.
        :return: Lista de tareas.
        """
        return self.tareas
    
    def obtener_estadisticas(self):
        """
        Calcula y devuelve estadísticas sobre las tareas.
        :return: Diccionario con el tiempo total, tiempo completado y porcentaje completado.
        """
        return {
            'tiempo_total': self.tiempo_total,  # Tiempo total de todas las tareas.
            'tiempo_completado': self.tiempo_completado,  # Tiempo total de las tareas completadas.
            'porcentaje_completado': (self.tiempo_completado / self.tiempo_total * 100) if self.tiempo_total > 0 else 0  # Porcentaje de tareas completadas.
        }