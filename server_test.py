from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP
from checksum import *
import time
from client_test import test_cliente
from multiprocessing import Process
import matplotlib.pyplot as plt

def test_servidor(cant_paquetes) -> List:

    # interface = "lo0" 
    interface = "Software Loopback Interface 1"

    listen_port = 8000  

    paquetes_sin_delay = 0
    paquetes_con_delay = 0

    cant_corruptos = 0

    tiempos_entrega = []

    conectado = True

    cuenta = 0

    while conectado:

        print(f"Listening for TCP packets on port {listen_port}...")
        filter_str = f"tcp port {listen_port}"
        
        start = time.time() # Se guarda el tiempo en el que empezó a escuchar el servidor

        cuenta += 1
        
        pkt_capturado = sniff(iface = interface, filter=filter_str, count=1, timeout=8) 

        if pkt_capturado: # Si capturó un paquete sin delay

            end = time.time() # Se guarda el tiempo en el que llegó el paquete
            tiempos_entrega.append(end-start) # Se guarda el tiempo que tardó en llegar el paquete en la lista

            # paquetes_sin_delay += 1

            paquete = pkt_capturado[0]
            flag = paquete[TCP].flags

            flags_esperadas = ("S", "A", "FA")

            if not(flag in flags_esperadas):
                continue 

            # Checksum

            tcp_checksum = paquete[TCP].chksum

            paquete[TCP].chksum = 0
            ph = pseudo_header(paquete[IP].src, paquete[IP].dst, paquete[IP].proto, len(paquete[TCP]))
            checksum_calculado = checksum(bytes(paquete[TCP]) + ph)
            print(checksum_calculado)
            print(tcp_checksum)

            if tcp_checksum != checksum_calculado:
                cant_corruptos += 1
                continue # Sigue escuchando

        if cuenta >= cant_paquetes + 2:
            conectado = False

    print("Fin de la conexión")

    paquetes_recibidos = len(tiempos_entrega)
    paquetes_perdidos = cant_paquetes - paquetes_recibidos

    i = 0
    while i < len(tiempos_entrega):
        if tiempos_entrega[i] < 3:
            tiempos_entrega.remove(tiempos_entrega[i])
            paquetes_sin_delay += 1
        else:
            i += 1

    paquetes_con_delay = len(tiempos_entrega) / cant_paquetes # % de paquetes con delay

    delay_promedio = 0
    for tiempo in tiempos_entrega:
        delay_promedio = delay_promedio + tiempo
    delay_promedio = delay_promedio/len(tiempos_entrega)

    valores_relevantes = []
    valores_relevantes.append(paquetes_recibidos)
    valores_relevantes.append(paquetes_perdidos)
    valores_relevantes.append(paquetes_sin_delay)
    valores_relevantes.append(paquetes_con_delay) 
    valores_relevantes.append(delay_promedio)   
    valores_relevantes.append(cant_corruptos)
    print (valores_relevantes)

    return valores_relevantes

def grafico_delay():
    if __name__ == '__main__':
        aux = 1
        eje_x = []
        eje_y = []
        while aux < 5:
            p1 = Process(target=test_servidor(aux))
            p2 = Process(target=test_cliente(aux))
            p1.start()
            p2.start()
            eje_x.append(aux)
            eje_y.append(p1[3])
            aux += 1
    
    plt.bar(eje_x, eje_y)
    plt.title('Porcentaje de paquetes que llegan con delay')
    plt.xlabel('Cantidad de paquetes recibidos')
    plt.ylabel('Porcentaje de paquetes que llegaron con delay')
    plt.show()
    return






