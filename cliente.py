import canalruidoso as f 
from scapy.all import * 
from scapy.all import TCP, IP
import time
import random
from funcionesAuxiliares import *

retransmisiones_finack = 0 # una herramienta misteriosa que nos ayudará más tarde

# Elegimos parametros
source_ip = '127.0.0.1'
dest_ip = '127.0.0.1'
dest_port = 8000
src_port = 5000

num_seq = random.randint(1, 10000) 
num_ack = 0

print(num_seq)

ip = IP(dst=dest_ip,src =source_ip)
tcp = TCP(dport=dest_port, sport =src_port, seq=num_seq, ack=num_ack, flags="S")
syn_packet = ip/tcp 

ultimo_packet_enviado = "SYN"

f.envio_paquetes_inseguro(syn_packet) # Se envía el paquete que contiene el SYN.

interface = "Software Loopback Interface 1" 
# interface = "lo0"

listen_port = 5000  

conectado = True 

print(f"Listening for TCP packets on port {listen_port}...")
filter_str = f"tcp port {listen_port}"

while conectado: # Acá manejamos todo lo que pasa después de que se envia el SYN

    print(f"Listening for TCP packets on port {listen_port}...")
    filter_str = f"tcp port {listen_port}"

    pkt_capturado = sniff(iface = interface, filter=filter_str, count=1, timeout=10) 

    if pkt_capturado: # Si capturó un paquete sin delay

        print(pkt_capturado)

        paquete = pkt_capturado[0]

        flag = paquete[TCP].flags

        flags_esperadas = ("SA", "A", "F")

        if not(flag in flags_esperadas):
            continue # Paso a la siguiente iteración

        pkt_capturado.show()

        # Checksum
        '''
        # ip_checksum = paquete[IP].chksum
        tcp_checksum = paquete[TCP].chksum

        # print(f"Checksum IP del paquete con la flag {flag}: {ip_checksum}")
        print(f"Checksum TCP del paquete con la flag {flag}: {tcp_checksum}")

        if ip_checksum != 0 or tcp_checksum != 0:
            print(f"El paquete con la flag {flag} está corrupto")
            # Tengo que retransmitir
        else:
        '''

        if flag == "SA": # Si recibe un SYN+ACK, manda un ACK
            ip = IP(dst=dest_ip,src =source_ip)
            tcp = TCP(dport=dest_port, sport =src_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="A")
            ack_packet = ip/tcp 
            ultimo_packet_enviado = "ACK"
            f.envio_paquetes_inseguro(ack_packet) # Se envía el paquete que contiene el ACK

        elif flag == "F":
            ip = IP(dst=dest_ip,src =source_ip)
            tcp = TCP(dport=dest_port, sport =src_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="FA")
            finack_packet = ip/tcp 
            ultimo_packet_enviado = "FIN_ACK"
            f.envio_paquetes_inseguro(finack_packet) # Se envía el paquete que contiene el FIN+ACK 

        elif flag == "A": # Recibe el último ACK. Ya se puede cerrar la conexión
            conectado = False
            
        else:
            continue 
                
    else: # Si pasaron 3 segundos y no recibí ningún paquete
        
        if ultimo_packet_enviado == "SYN": # Retransmito el paquete SYN
            f.envio_paquetes_inseguro(syn_packet)
            
        elif ultimo_packet_enviado == "ACK": # Retransmito el paquete ACK
            f.envio_paquetes_inseguro(ack_packet)

        elif ultimo_packet_enviado == "FIN_ACK":
            '''
            El cliente retransmitirá el FIN ACK varias veces. Si después de un número determinado de retransmisiones 
            aún no recibe el ACK, el cliente terminará cerrando la conexión de manera unilateral, agotando su temporizador.
            '''
            if retransmisiones_finack < 5:
                f.envio_paquetes_inseguro(finack_packet)
                retransmisiones_finack += 1
            else:
                conectado = False # Cierro la conexión
                
        else: # Paso a la siguiente iteración
            continue

        
    
print("Fin de la conexión")
            
   




















