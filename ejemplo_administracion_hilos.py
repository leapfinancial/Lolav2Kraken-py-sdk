"""
Ejemplo de administración de pesos y prioridades de hilos
"""

from lolakrakenpy.lola_kraken_utils_services import LolaUtilsServicesManager
import time

# Inicializar el gestor
session = {'lead': 'test_lead'}
utils_manager = LolaUtilsServicesManager(
    session=session,
    lola_token="your_token",
    lola_kraken_url="http://your-api-url",
    max_workers=10
)

# Ejemplos de administración de hilos con pesos/prioridades

def ejemplo_1_prioridades_basicas():
    """Ejemplo básico de uso de prioridades"""
    print("=== Ejemplo 1: Prioridades Básicas ===")
    
    # Ejecutar tareas con diferentes prioridades
    # Prioridad 1 = Muy Alta (se ejecuta primero)
    task_id_alta = utils_manager.execute_with_priority(
        priority=1, 
        func=ejemplo_tarea_pesada, 
        nombre="Tarea Alta Prioridad"
    )
    
    # Prioridad 5 = Media
    task_id_media = utils_manager.execute_with_priority(
        priority=5, 
        func=ejemplo_tarea_pesada, 
        nombre="Tarea Media Prioridad"
    )
    
    # Prioridad 10 = Baja
    task_id_baja = utils_manager.execute_with_priority(
        priority=10, 
        func=ejemplo_tarea_pesada, 
        nombre="Tarea Baja Prioridad"
    )
    
    print(f"Task IDs creados: {task_id_alta}, {task_id_media}, {task_id_baja}")
    
    # Monitorear el estado
    time.sleep(2)
    print("\nEstado de las tareas:")
    for task_id in [task_id_alta, task_id_media, task_id_baja]:
        status = utils_manager.get_thread_status(task_id)
        if status:
            print(f"Task {task_id}: Prioridad {status['priority']}, Estado: {status['status']}")

def ejemplo_2_gestion_de_pesos():
    """Ejemplo usando pesos en lugar de prioridades"""
    print("\n=== Ejemplo 2: Gestión por Pesos ===")
    
    # Usar pesos (peso alto = prioridad baja)
    task_liviana = utils_manager.execute_with_weight(
        weight=1,  # Peso bajo = alta prioridad
        func=ejemplo_tarea_ligera,
        nombre="Tarea Liviana"
    )
    
    task_media = utils_manager.execute_with_weight(
        weight=5,  # Peso medio = prioridad media
        func=ejemplo_tarea_pesada,
        nombre="Tarea Media"
    )
    
    task_pesada = utils_manager.execute_with_weight(
        weight=10,  # Peso alto = baja prioridad
        func=ejemplo_tarea_muy_pesada,
        nombre="Tarea Pesada"
    )
    
    # Ver hilos organizados por prioridad
    threads_by_priority = utils_manager.get_threads_by_priority()
    print(f"Hilos por prioridad: {threads_by_priority}")

def ejemplo_3_metricas_y_control():
    """Ejemplo de métricas y control de hilos"""
    print("\n=== Ejemplo 3: Métricas y Control ===")
    
    # Crear varias tareas
    for i in range(5):
        utils_manager.execute_with_priority(
            priority=i + 1,
            func=ejemplo_tarea_pesada,
            nombre=f"Tarea {i}"
        )
    
    # Obtener métricas
    metrics = utils_manager.get_thread_metrics()
    print(f"Métricas actuales: {metrics}")
    
    # Pausar hilos de baja prioridad (>= 4)
    paused = utils_manager.pause_low_priority_threads(threshold_priority=4)
    print(f"Hilos pausados: {paused}")
    
    # Limpiar hilos completados
    utils_manager.cleanup_completed_threads()
    print("Hilos completados limpiados")

def ejemplo_4_notificaciones_con_prioridad():
    """Ejemplo usando notificaciones con diferentes prioridades"""
    print("\n=== Ejemplo 4: Notificaciones con Prioridad ===")
    
    # Notificación crítica (prioridad 1)
    task_critica = utils_manager.threadSendNotification(
        reqToken="token123",
        label="notificacion_critica",
        payload={"mensaje": "Error crítico del sistema"},
        priority=1  # Máxima prioridad
    )
    
    # Notificación normal (prioridad 5)
    task_normal = utils_manager.threadSendNotification(
        reqToken="token123",
        label="notificacion_normal",
        payload={"mensaje": "Información general"},
        priority=5
    )
    
    # Notificación de baja prioridad (prioridad 10)
    task_baja = utils_manager.threadSendNotification(
        reqToken="token123",
        label="notificacion_baja",
        payload={"mensaje": "Log informativo"},
        priority=10
    )
    
    print(f"Notificaciones enviadas: {task_critica}, {task_normal}, {task_baja}")

def ejemplo_5_cambio_dinamico_prioridad():
    """Ejemplo de cambio dinámico de prioridades"""
    print("\n=== Ejemplo 5: Cambio Dinámico de Prioridad ===")
    
    # Crear una tarea con prioridad baja
    task_id = utils_manager.execute_with_priority(
        priority=10,
        func=ejemplo_tarea_muy_pesada,
        nombre="Tarea que cambiará prioridad"
    )
    
    print(f"Tarea creada con prioridad 10: {task_id}")
    
    time.sleep(1)
    
    # Cambiar a alta prioridad
    changed = utils_manager.set_thread_priority(task_id, 1)
    if changed:
        print(f"Prioridad de {task_id} cambiada a 1")
    
    # Verificar el cambio
    status = utils_manager.get_thread_status(task_id)
    if status:
        print(f"Nueva prioridad: {status['priority']}")

# Funciones de ejemplo para las tareas
def ejemplo_tarea_ligera(nombre):
    print(f"Ejecutando {nombre} (tarea ligera)")
    time.sleep(1)
    print(f"Completada {nombre}")

def ejemplo_tarea_pesada(nombre):
    print(f"Ejecutando {nombre} (tarea pesada)")
    time.sleep(3)
    print(f"Completada {nombre}")

def ejemplo_tarea_muy_pesada(nombre):
    print(f"Ejecutando {nombre} (tarea muy pesada)")
    time.sleep(5)
    print(f"Completada {nombre}")

if __name__ == "__main__":
    # Ejecutar ejemplos (descomenta el que quieras probar)
    
    # ejemplo_1_prioridades_basicas()
    # ejemplo_2_gestion_de_pesos()
    # ejemplo_3_metricas_y_control()
    # ejemplo_4_notificaciones_con_prioridad()
    # ejemplo_5_cambio_dinamico_prioridad()
    
    # Limpiar al final
    time.sleep(10)  # Esperar a que terminen las tareas
    utils_manager.shutdown_thread_pool()
    print("\nPool de hilos cerrado")
