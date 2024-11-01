import matplotlib.pyplot as plt
from client_test import *
from server_test import *
from multiprocessing import Process

if __name__ == '__main__':
    p1 = Process(target=test_servidor)
    p2 = Process(target=test_cliente)
    p1.start()
    p2.start()

'''
Tenemos que hacer que las funciones devuelvan la info que necesitamos para graficar y despues graficar

Para el eje x y el eje y de un grafico hay que poner la data en LISTAS

'''



