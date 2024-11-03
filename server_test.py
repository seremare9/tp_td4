from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP
from checksum import *
import time
from client_test import test_cliente
from multiprocessing import Process

def test_servidor(cant_paquetes) -> List:

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

            paquete = pkt_capturado[0]

            # Se fija que las flags del paquete sean las correspondientes al handshake y/o al cierre
            flag = paquete[TCP].flags

            flags_esperadas = ("S", "A", "FA")

            if not(flag in flags_esperadas):
                continue 

            # Checksum
            tcp_checksum = paquete[TCP].chksum

            paquete[TCP].chksum = 0
            ph = pseudo_header(paquete[IP].src, paquete[IP].dst, paquete[IP].proto, len(paquete[TCP])) # Arma un pseudo header con los datos del paquete
            checksum_calculado = checksum(bytes(paquete[TCP]) + ph) # Recalcula el checksum usando el pseudo header y los bytes del paquete TCP
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
    
    paquete_mas_rapido = min(tiempos_entrega)

    # Se remueven los tiempos de entrega de los paquetes que no tuvieron delay de la lista
    i = 0
    while i < len(tiempos_entrega):
        if tiempos_entrega[i] < 3:
            tiempos_entrega.remove(tiempos_entrega[i])
            paquetes_sin_delay += 1
        else:
            i += 1

    paquetes_con_delay = len(tiempos_entrega)

    # Se calcula el delay promedio con los valores que quedan en la lista
    delay_promedio = 0
    if len(tiempos_entrega) != 0:
        for tiempo in tiempos_entrega:
            delay_promedio = delay_promedio + tiempo
        delay_promedio = delay_promedio/len(tiempos_entrega)

    paquete_mas_lento = max(tiempos_entrega)
    
    # Se imprimen todos los valores que consideramos relevantes para la experimentación
    print(f"Cantidad de paquetes enviados: {cant_paquetes} ")
    print(f"Cantidad de paquetes recibidos: {paquetes_recibidos}")
    print(f"Cantidad de paquetes perdidos: {paquetes_perdidos}")
    print(f"Cantidad de paquetes sin delay: {paquetes_sin_delay} ")
    print(f"Cantidad de paquetes con delay: {paquetes_con_delay} ")
    print(f"Menor delay: {paquete_mas_rapido}")
    print(f"Mayor delay: {paquete_mas_lento}")
    print(f"Delay promedio: {delay_promedio}")
    print(f"Cantidad de paquetes corruptos: {cant_corruptos} ")


# Se ejecutan el test del cliente y el servidor en simultáneo
if __name__ == '__main__':
    p1 = Process(target=test_servidor, args=(25,)) # El valor del argumento se cambia a mano para la experimentación con cada cantidad de paquetes
    p2 = Process(target=test_cliente, args=(25,)) # El valor del argumento se cambia a mano para la experimentación con cada cantidad de paquetes
    p1.start()
    p2.start()
