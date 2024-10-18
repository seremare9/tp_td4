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

f.envio_paquetes_inseguro(syn_packet)

# while respuesta == False: 
#     pkt_capturado = sniff(iface = "lo0", prn=lambda x: x.show(), count=1, timeout=3)
#     if pkt_capturado:
#         respuesta = True
#     else:
#         f.envio_paquetes_inseguro(syn_packet) # Retransmito el packet

# Examino el packet recibido y mando ACK





