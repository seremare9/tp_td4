from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP
from checksum import *
import random

def test_cliente(cant_paquetes):

    flags = ["S", "A", "FA"]

    i = 0

    while i < cant_paquetes:
        num_seq = random.randint(1, 10000) # Se elige un número de secuencia al azar para el paquete
        ip = IP(dst='127.0.0.1',src ='127.0.0.1')
        tcp = TCP(dport=8000, sport =5000, seq=num_seq, ack=0, flags=random.choice(flags))
        paquete = ip/tcp 
        f.envio_paquetes_inseguro(paquete) # Se envía paquete al servidor
        i = i+1
    
    return