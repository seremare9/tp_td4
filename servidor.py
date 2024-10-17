from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP

# print(conf.ifaces)

interface = "lo0" # loopback en Mac 

listen_port = 8000  # Elegir el puerto que esta escuchando

print(f"Listening for TCP packets on port {listen_port}...")
filter_str = f"tcp port {listen_port}"

tiempo = 10 # vamos probando con distintos valores

# Escuchar en ese puerto
pkt_capturado = sniff(iface = interface, filter=filter_str, prn=lambda x: x.show(), count=1, timeout=tiempo)

if not pkt_capturado:
    print("No llego nada")


# reviso el packet recibido y mando el packet SYN ACK
# checksum = pkt_capturado.compute_chksum()
'''
source_ip = '127.0.0.1'
dest_ip = '127.0.0.1'
dest_port = 5000 #puerto del cliente
src_port = 8000 #puerto del server

num_seq = 0

num_ack = 0

ip = IP(dst=dest_ip,src =source_ip)

tcp = TCP(dport=dest_port, sport =src_port, seq=num_seq, ack=num_ack, flags="S")

syn_ack_packet = ip/tcp

f.envio_paquetes_inseguro(syn_ack_packet)

# Aca tengo que implementar el mismo sistema de retransmisiones que el cliente
'''