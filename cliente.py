import canalruidoso as f 
from scapy.all import * 
from scapy.all import TCP, IP
import time
import random

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

respuesta = False

# print("Imprimo packet")
# syn_packet.show()
# print("Fin packet")

f.envio_paquetes_inseguro(syn_packet) # Se envía el paquete que contiene el SYN.


interface = "Software Loopback Interface 1"

listen_port = 5000  

print(f"Listening for TCP packets on port {listen_port}...")
filter_str = f"tcp port {listen_port}" 

pkt_capturado = sniff(iface = interface, prn=lambda x: x.show(), timeout=120) # El cliente se queda escuchando en el puerto 5000

if pkt_capturado:

    paquete = pkt_capturado[0]
    flag = paquete[TCP].flags

    # Checksum
    if paquete[IP].chksum == paquete[IP].calc_chksum():
        error_checksum = False # Llego ok
    else:
        error_checksum = True # como procedemos?
        

    if flag == "SA": # Si recibe un SYN+ACK, manda un ACK
        paquete = pkt_capturado[0] # Recibe paquete del servidor con SYN+ACK

        ip = IP(dst=dest_ip,src =source_ip)
        tcp = TCP(dport=dest_port, sport =src_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="A")
        ack_packet = ip/tcp 

        f.envio_paquetes_inseguro(ack_packet) # Se envía el paquete que contiene el ACK

    elif flag == "F":
        paquete = pkt_capturado[0] # Recibe paquete del servidor con FIN

        ip = IP(dst=dest_ip,src =source_ip)
        tcp = TCP(dport=dest_port, sport =src_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="FA")
        finack_packet = ip/tcp 

        f.envio_paquetes_inseguro(finack_packet) # Se envía el paquete que contiene el FIN+ACK    

# while respuesta == False: 
#     pkt_capturado = sniff(iface = "lo0", prn=lambda x: x.show(), count=1, timeout=3)
#     if pkt_capturado:
#         respuesta = True
#     else:
#         f.envio_paquetes_inseguro(syn_packet) # Retransmito el packet

# Examino el packet recibido y mando ACK





