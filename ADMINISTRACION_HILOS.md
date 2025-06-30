# Administración de Pesos y Prioridades de Hilos

## Conceptos Básicos

### Prioridades vs Pesos
- **Prioridad**: Número menor = mayor prioridad (1 = máxima prioridad, 10 = baja prioridad)
- **Peso**: Número mayor = menor prioridad (1 = liviano/alta prioridad, 10 = pesado/baja prioridad)

## Métodos Principales

### 1. `execute_with_priority(priority, func, *args, **kwargs)`
Ejecuta una función con una prioridad específica.

```python
# Prioridad alta (1)
task_id = utils_manager.execute_with_priority(1, mi_funcion, arg1, arg2)

# Prioridad media (5)
task_id = utils_manager.execute_with_priority(5, mi_funcion, arg1, arg2)
```

### 2. `execute_with_weight(weight, func, *args, **kwargs)`
Ejecuta una función usando el concepto de "peso" (peso alto = prioridad baja).

```python
# Peso bajo = alta prioridad
task_id = utils_manager.execute_with_weight(1, tarea_critica)

# Peso alto = baja prioridad
task_id = utils_manager.execute_with_weight(10, tarea_background)
```

### 3. `set_thread_priority(task_id, new_priority)`
Cambia la prioridad de un hilo en ejecución.

```python
# Cambiar prioridad dinámicamente
success = utils_manager.set_thread_priority("task_123", 1)
```

## Métodos de Monitoreo

### 1. `get_thread_status(task_id)`
Obtiene el estado de un hilo específico.

```python
status = utils_manager.get_thread_status("task_123")
if status:
    print(f"Prioridad: {status['priority']}")
    print(f"Estado: {status['status']}")
```

### 2. `get_threads_by_priority()`
Organiza todos los hilos por prioridad.

```python
threads = utils_manager.get_threads_by_priority()
for priority, thread_list in threads.items():
    print(f"Prioridad {priority}: {len(thread_list)} hilos")
```

### 3. `get_thread_metrics()`
Obtiene métricas completas del sistema de hilos.

```python
metrics = utils_manager.get_thread_metrics()
print(f"Hilos activos: {metrics['running_threads']}")
print(f"Prioridad promedio: {metrics['average_priority']}")
print(f"Workers disponibles: {metrics['available_workers']}")
```

## Métodos de Control

### 1. `pause_low_priority_threads(threshold_priority)`
Pausa hilos con prioridad baja.

```python
# Pausar hilos con prioridad >= 5
paused = utils_manager.pause_low_priority_threads(5)
print(f"Hilos pausados: {paused}")
```

### 2. `cancel_thread(task_id)`
Cancela un hilo específico.

```python
cancelled = utils_manager.cancel_thread("task_123")
if cancelled:
    print("Hilo cancelado exitosamente")
```

### 3. `cleanup_completed_threads()`
Limpia hilos completados del registro.

```python
utils_manager.cleanup_completed_threads()
```

## Casos de Uso Comunes

### 1. Sistema de Notificaciones por Prioridad

```python
# Notificación crítica
utils_manager.threadSendNotification(
    reqToken="token",
    label="error_critico",
    payload={"error": "Sistema caído"},
    priority=1  # Máxima prioridad
)

# Notificación informativa
utils_manager.threadSendNotification(
    reqToken="token",
    label="info",
    payload={"mensaje": "Proceso completado"},
    priority=5  # Prioridad media
)
```

### 2. Gestión de Carga de Trabajo

```python
# Tareas críticas del sistema
for critical_task in critical_tasks:
    utils_manager.execute_with_priority(1, process_critical, critical_task)

# Tareas de mantenimiento
for maintenance_task in maintenance_tasks:
    utils_manager.execute_with_priority(10, process_maintenance, maintenance_task)
```

### 3. Balanceador de Carga Dinámico

```python
def balance_load():
    metrics = utils_manager.get_thread_metrics()
    
    # Si hay muchos hilos activos, pausar los de baja prioridad
    if metrics['running_threads'] > 8:
        utils_manager.pause_low_priority_threads(7)
    
    # Limpiar hilos completados periodicamente
    if metrics['completed_threads'] > 20:
        utils_manager.cleanup_completed_threads()
```

## Mejores Prácticas

### 1. Definir Niveles de Prioridad Estándar
```python
class Priority:
    CRITICAL = 1    # Errores críticos, alertas de seguridad
    HIGH = 2        # Tareas importantes del usuario
    NORMAL = 5      # Operaciones estándar
    LOW = 8         # Tareas de background
    MAINTENANCE = 10 # Limpieza, logs, estadísticas
```

### 2. Monitoreo Continuo
```python
def monitor_threads():
    while True:
        metrics = utils_manager.get_thread_metrics()
        if metrics['running_threads'] == 0 and metrics['queue_size'] > 0:
            utils_manager.process_priority_queue()
        time.sleep(5)
```

### 3. Gestión de Recursos
```python
def resource_management():
    # Limitar hilos de baja prioridad si el sistema está sobrecargado
    if system_load() > 0.8:
        utils_manager.pause_low_priority_threads(6)
    
    # Incrementar workers si hay mucha cola
    metrics = utils_manager.get_thread_metrics()
    if metrics['queue_size'] > 20:
        # Considerr aumentar max_workers o pausar tareas no críticas
        pass
```

## Consideraciones de Rendimiento

1. **Overhead**: El sistema de prioridades añade overhead mínimo
2. **Memoria**: Los hilos completados deben limpiarse regularmente
3. **Concurrencia**: El semáforo controla la concurrencia máxima
4. **Deadlocks**: Los locks están diseñados para evitar deadlocks

## Debugging y Troubleshooting

```python
def debug_thread_system():
    print("=== Estado del Sistema de Hilos ===")
    
    # Métricas generales
    metrics = utils_manager.get_thread_metrics()
    for key, value in metrics.items():
        print(f"{key}: {value}")
    
    # Hilos por prioridad
    threads = utils_manager.get_threads_by_priority()
    print(f"\nHilos por prioridad: {threads}")
    
    # Estado de hilos individuales
    print(f"\nHilos activos: {utils_manager.get_active_threads_count()}")
```
