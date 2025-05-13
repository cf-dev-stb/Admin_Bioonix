class Tarea:
    def __init__(self, nombre, tiempo):
        self.nombre = nombre
        self.tiempo = tiempo
        self.completado = False

class ModeloTareas:
    def __init__(self):
        self.tareas = []
        self.tiempo_total = 0
        self.tiempo_completado = 0
    
    def agregar_tarea(self, nombre, tiempo):
        tarea = Tarea(nombre, tiempo)
        self.tareas.append(tarea)
        self.tiempo_total += tiempo
        return tarea
    
    def marcar_completado(self, nombre_tarea):
        for tarea in self.tareas:
            if tarea.nombre == nombre_tarea and not tarea.completado:
                tarea.completado = True
                self.tiempo_completado += tarea.tiempo
                return True
        return False
    
    def eliminar_tarea(self, nombre_tarea):
        for tarea in self.tareas:
            if tarea.nombre == nombre_tarea:
                if tarea.completado:
                    self.tiempo_completado -= tarea.tiempo
                self.tiempo_total -= tarea.tiempo
                self.tareas.remove(tarea)
                return True
        return False
    
    def obtener_todas_tareas(self):
        return self.tareas
    
    def obtener_estadisticas(self):
        return {
            'tiempo_total': self.tiempo_total,
            'tiempo_completado': self.tiempo_completado,
            'porcentaje_completado': (self.tiempo_completado / self.tiempo_total * 100) if self.tiempo_total > 0 else 0
        }