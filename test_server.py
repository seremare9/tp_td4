from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP
from funcionesAuxiliares import *
import time

# interface = "lo0" 
interface = "Software Loopback Interface 1"

listen_port = 8000  

paquetes_sin_delay = 0
paquetes_con_delay = 0

cant_corruptos = 0

conectado = True

while conectado:

    print(f"Listening for TCP packets on port {listen_port}...")
    filter_str = f"tcp port {listen_port}"

    pkt_capturado = sniff(iface = interface, filter=filter_str, count=1, timeout=3) 

    if pkt_capturado: # Si capturó un paquete sin delay

        paquetes_sin_delay += 1

        paquete = pkt_capturado[0]
        flag = paquete[TCP].flags

        flags_esperadas = ("S", "A", "FA")

        if not(flag in flags_esperadas):
            continue 

        # Checksum

        tcp_checksum = paquete[TCP].chksum

        paquete[TCP].chksum = 0
        # paquete = paquete.__class__(bytes(paquete))
        ph = pseudo_header(paquete[IP].src, paquete[IP].dst, paquete[IP].proto, len(paquete[TCP]))
        checksum_calculado = checksum(bytes(paquete[TCP]) + ph)
        print(checksum_calculado)

        if tcp_checksum != checksum_calculado:
            cant_corruptos += 1
            continue # Sigue escuchando


    else: # Si pasaron 3 segundos y no recibí ningún paquete
        
        paquetes_con_delay += 1

        

print("Fin de la conexión")




































'''

Escucha

cuando le llega le manda un ack por scapy normal





'''

