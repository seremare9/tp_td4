import matplotlib.pyplot as plt
from client_test import *
from server_test import *
from multiprocessing import Process

if __name__ == '__main__':

    queue = Queue()
    p1 = Process(target=test_servidor, rgs=(queue,))
    p2 = Process(target=test_cliente)
    p1.start()
    p2.start()

    # Obtener el resultado de test_servidor desde la cola
    resultado_servidor = queue.get()

    # Esperar a que los procesos terminen
    p1.join()
    p2.join()

    print(type(resultado_servidor))

    tiempos_entrega = resultado_servidor["tiempos_entrega"]
    cant_corruptos = resultado_servidor["corruptos"]
    paquetes_con_delay = resultado_servidor["delayed"]
    paquetes_sin_delay = resultado_servidor["not_delayed"]

    print(type(tiempos_entrega))
    print(type(cant_corruptos))
    print(type(paquetes_con_delay))
    print(type(paquetes_sin_delay))

    # Si todos los tipos son LISTAS, podemos empezar a graficar

    




