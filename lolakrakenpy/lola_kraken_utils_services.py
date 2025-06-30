import threading
import requests
import queue
import time
from concurrent.futures import ThreadPoolExecutor
from lolakrakenpy.shemas.utils_shema import RequestExtradataParams, SendNotificationSchema, claimTokenSchema,claimTokenUrlSchema, validateAddressSchema


class LolaUtilsServicesManager:
    def __init__(self, session, lola_token, lola_kraken_url, max_workers=20):
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url
        self.session = session
        # Pool de hilos para gestionar la carga
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        # Cola de prioridad para tareas
        self.priority_queue = queue.PriorityQueue()
        # Control de hilos activos
        self.active_threads = {}
        self.thread_counter = 0
        # Lock para operaciones thread-safe
        self.thread_lock = threading.Lock()
        # Semáforo para controlar concurrencia
        self.semaphore = threading.Semaphore(max_workers)
        
    def add_priority_task(self, priority, func, *args, **kwargs):
        """
        Añade una tarea con prioridad a la cola
        Args:
            priority (int): Prioridad (menor número = mayor prioridad)
            func: Función a ejecutar
            *args, **kwargs: Argumentos para la función
        """
        task_id = f"task_{self.thread_counter}"
        self.thread_counter += 1
        # El PriorityQueue ordena por el primer elemento de la tupla (prioridad)
        self.priority_queue.put((priority, task_id, func, args, kwargs))
        return task_id
    
    def process_priority_queue(self):
        """
        Procesa las tareas de la cola de prioridad
        """
        while not self.priority_queue.empty():
            try:
                priority, task_id, func, args, kwargs = self.priority_queue.get_nowait()
                future = self.executor.submit(self._execute_with_semaphore, func, args, kwargs)
                with self.thread_lock:
                    self.active_threads[task_id] = {
                        'future': future,
                        'priority': priority,
                        'status': 'running'
                    }
            except queue.Empty:
                break
    
    def _execute_with_semaphore(self, func, args, kwargs):
        """
        Ejecuta una función con control de semáforo
        """
        with self.semaphore:
            return func(*args, **kwargs)
    
    def get_thread_status(self, task_id):
        """
        Obtiene el estado de un hilo específico
        """
        with self.thread_lock:
            if task_id in self.active_threads:
                thread_info = self.active_threads[task_id]
                if thread_info['future'].done():
                    thread_info['status'] = 'completed'
                return thread_info
        return None
    
    def cancel_thread(self, task_id):
        """
        Cancela un hilo específico si es posible
        """
        with self.thread_lock:
            if task_id in self.active_threads:
                future = self.active_threads[task_id]['future']
                cancelled = future.cancel()
                if cancelled:
                    self.active_threads[task_id]['status'] = 'cancelled'
                return cancelled
        return False
    
    def get_active_threads_count(self):
        """
        Obtiene el número de hilos activos
        """
        with self.thread_lock:
            active_count = sum(1 for thread in self.active_threads.values() 
                             if thread['status'] == 'running')
        return active_count
    
    def cleanup_completed_threads(self):
        """
        Limpia los hilos completados del registro
        """
        with self.thread_lock:
            completed_tasks = [task_id for task_id, thread_info in self.active_threads.items()
                             if thread_info['future'].done()]
            for task_id in completed_tasks:
                del self.active_threads[task_id]
    
    def shutdown_thread_pool(self, wait=True):
        """
        Cierra el pool de hilos
        """
        self.executor.shutdown(wait=wait)
    
    def set_thread_priority(self, task_id, new_priority):
        """
        Cambia la prioridad de un hilo en ejecución
        Args:
            task_id: ID de la tarea
            new_priority: Nueva prioridad
        """
        with self.thread_lock:
            if task_id in self.active_threads:
                self.active_threads[task_id]['priority'] = new_priority
                return True
        return False
    
    def get_threads_by_priority(self):
        """
        Obtiene todos los hilos organizados por prioridad
        """
        with self.thread_lock:
            threads_by_priority = {}
            for task_id, thread_info in self.active_threads.items():
                priority = thread_info['priority']
                if priority not in threads_by_priority:
                    threads_by_priority[priority] = []
                threads_by_priority[priority].append({
                    'task_id': task_id,
                    'status': thread_info['status']
                })
        return threads_by_priority
    
    def execute_with_priority(self, priority, func, *args, **kwargs):
        """
        Ejecuta una función con prioridad específica inmediatamente
        Args:
            priority: Prioridad de la tarea
            func: Función a ejecutar
        Returns:
            Future object para monitorear la ejecución
        """
        task_id = self.add_priority_task(priority, func, *args, **kwargs)
        self.process_priority_queue()
        return task_id
    
    def execute_with_weight(self, weight, func, *args, **kwargs):
        """
        Ejecuta una función con peso específico (peso alto = prioridad baja)
        Args:
            weight: Peso de la tarea (número alto = menor prioridad)
            func: Función a ejecutar
        Returns:
            Task ID para monitorear la ejecución
        """
        # Convertir peso a prioridad (peso alto = prioridad baja)
        priority = weight
        return self.execute_with_priority(priority, func, *args, **kwargs)
    
    def get_thread_metrics(self):
        """
        Obtiene métricas de los hilos activos
        """
        with self.thread_lock:
            total_threads = len(self.active_threads)
            running_threads = sum(1 for t in self.active_threads.values() if t['status'] == 'running')
            completed_threads = sum(1 for t in self.active_threads.values() if t['status'] == 'completed')
            cancelled_threads = sum(1 for t in self.active_threads.values() if t['status'] == 'cancelled')
            
            priorities = [t['priority'] for t in self.active_threads.values()]
            avg_priority = sum(priorities) / len(priorities) if priorities else 0
            
            return {
                'total_threads': total_threads,
                'running_threads': running_threads,
                'completed_threads': completed_threads,
                'cancelled_threads': cancelled_threads,
                'average_priority': avg_priority,
                'queue_size': self.priority_queue.qsize(),
                'available_workers': self.semaphore._value
            }
    
    def pause_low_priority_threads(self, threshold_priority=5):
        """
        Pausa hilos con prioridad baja (número alto)
        Args:
            threshold_priority: Umbral de prioridad para pausar
        """
        paused_threads = []
        with self.thread_lock:
            for task_id, thread_info in self.active_threads.items():
                if thread_info['priority'] >= threshold_priority and thread_info['status'] == 'running':
                    if self.cancel_thread(task_id):
                        paused_threads.append(task_id)
        return paused_threads

    def claimToken(self, metadata=None, sessionStore=None, extradata=None):
        """
        Claims a token.
        Args:
            token (str): The token to claim.
        Returns:
            dict: The response JSON.
        """
        try:
            session = self.session
            print(session)

            chatlead = None
            sessionStore = None
            
            try:
                chatlead = session['lead']
                sessionStore = sessionStore
            except:
                print("No session found")
                pass

            endpoint = f'{self.lola_kraken_url}/utils/claim/token'
            headers = {
                'x-lola-auth': self.lola_token,
                'Content-Type': 'application/json'
            }
            data = {
                'chatLead': chatlead,
                'sessionStore': sessionStore,
                'metadata': metadata,
                'extradata': extradata
            }
            data = claimTokenSchema(**data).model_dump(exclude_none=True)
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)

    def claimLink(self, link: str, metadata=None, sessionStore=None,extraData=None):
        """
        Claims a Link

        Args:
            Link (str): The Link to claim.
        Returns:
            dict: The response JSON.

        """
        try:
            session = self.session
            print(session)
            chatlead = session['lead']
            sessionStore = sessionStore
            endpoint = f'{self.lola_kraken_url}/utils/claim/link'
            headers = {
                'x-lola-auth': self.lola_token,
                'Content-Type': 'application/json'
            }
            data = {
                'baseUrl': link,
                'chatLead': chatlead,
                'sessionStore': sessionStore,
                'metadata': metadata,
                'extradata': extraData
            }
            data = claimTokenUrlSchema(**data).model_dump(exclude_none=True)
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)

    def validateAddress(self, address: str):
        """
        Validates an address.
        Args:
            address (str): The address to validate.
        Returns:
            dict: The response JSON.
        """
        try:
            endpoint = f'{self.lola_kraken_url}/utils/verify-address/{address}'
            headers = {
                'x-lola-auth': self.lola_token,
                'Content-Type': 'application/json'
            }

            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)

    def sendNotification(self, reqToken: str, label: str, payload):
        """
        Validates an address.
        Args:
            reqToken (str): Token with basic user data.
            label (str): Label of the notification.
            payload (object): Payload of the notification.
        Returns:
            dict: The response JSON.
        """
        try:
            endpoint = f'{self.lola_kraken_url}/utils/sendnotification'
            headers = {
                'Content-Type': 'application/json',
                'x-notification-token': reqToken
            }

            data = {
                'label': label,
                'payload': payload
            }
            data = SendNotificationSchema(**data).model_dump(exclude_none=True)

            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)
    def threadSendNotification(self, reqToken: str, label: str, payload, priority: int = 3):
        """
        Ejecuta sendNotification en un hilo con prioridad específica
        Args:
            reqToken: Token de notificación
            label: Etiqueta de la notificación
            payload: Datos de la notificación
            priority: Prioridad del hilo (menor número = mayor prioridad)
        """
        return self.execute_with_priority(priority, self.sendNotification, reqToken, label, payload)
    def validateAddress(self, address: str):
        """
        Validates an address.
        Args:
            address (str): The address to validate.
        Returns:
            dict: The response JSON.
        """
        try:
            endpoint = f'{self.lola_kraken_url}/utils/verify-address/{address}'
            headers = {
                'x-lola-auth': self.lola_token,
                'Content-Type': 'application/json'
            }

            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)
        
    def sendTokenIdNotification(self, tokenId: str, label: str, payload):
        """
        Send notification to token id.
        Args:
            tokenId (str): Token id to send notification.
            label (str): Label of the notification.
            payload (object): Payload of the notification.
        Returns:
            dict: The response JSON.
        """
        try:
            endpoint = f'{self.lola_kraken_url}/utils/send-token-id-notification'
            headers = {
                'Content-Type': 'application/json',
                'notification-token-id': tokenId,
            }

            data = {
                'label': label,
                'payload': payload
            }
            data = SendNotificationSchema(**data).model_dump(exclude_none=True)

            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)
    
    def threadSendTokenIdNotification(self, tokenId: str, label: str, payload, priority: int = 3):
        """
        Ejecuta sendTokenIdNotification en un hilo con prioridad específica
        Args:
            tokenId: ID del token
            label: Etiqueta de la notificación
            payload: Datos de la notificación
            priority: Prioridad del hilo (menor número = mayor prioridad)
        """
        return self.execute_with_priority(priority, self.sendTokenIdNotification, tokenId, label, payload)
        
    def sendNotificationToTokenId(self, tokenId: str, label: str, payload):
        """
        Validates an address.
        Args:
            reqToken (str): Token with basic user data.
            label (str): Label of the notification.
            payload (object): Payload of the notification.
        Returns:
            dict: The response JSON.
        """
        try:
            endpoint = f'{self.lola_kraken_url}/utils/send-notification/{tokenId}'
            headers = {
                'Content-Type': 'application/json',
            }

            data = {
                'label': label,
                'payload': payload
            }
            data = SendNotificationSchema(**data).model_dump(exclude_none=True)

            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)

    def getExtradata(self, reqToken: str):
        """
        Validates an address.
        Args:
            reqToken (str): Token with basic user data.
        Returns:
            dict: The response JSON.
        """
        try:
            endpoint = f'{self.lola_kraken_url}/utils/get-extradata'
            headers = {
                'x-lola-auth': self.lola_token,
                'Content-Type': 'application/json',
                'x-notification-token': reqToken
            }

            data = {
                'token': reqToken
            }
            data = RequestExtradataParams(**data).model_dump(exclude_none=True)

            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)
