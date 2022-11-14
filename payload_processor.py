import time
import _thread


def start():
    _thread.start_new_thread(local_security_loop, ())
    _thread.start_new_thread(local_processing_loop, ())


def process_payload(payload):
    """
    Ejecuta el procesamiento de un payload recibido
    """
    time.sleep(5)
    return True


def local_security_loop():
    '''
    Loop de seguridad local, nada puede activarse si no se cumple con las condiciones de seguridad local
    '''
    while True:
        pass
        # Leer estado de componentes de prioridad alta (Sensores de Nivel, Electrovalvulas, etc) [Diferente para cada nodo]

        # Aplicar medidas de seguridad en caso de ser necesario

        # Notificar al Gateway de los cambios de estado

def local_processing_loop():
    while True:
        pass
        # Leer estado de componentes

        # Aplicar medidas de seguridad en caso de ser necesario

        # Notificar al Gateway de los cambios de estado