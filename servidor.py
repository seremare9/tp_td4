from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP

# print(conf.ifaces)

interface = "lo0" # loopback en Mac, en Windows hay que usar otra (descomentar linea 5 para ver las opciones)

listen_port = 8000  

print(f"Listening for TCP packets on port {listen_port}...")
# filter_str = f"tcp port {listen_port}" 

tiempo = 30 # le puse un valor cualquiera

pkt_capturado = sniff(iface = interface, prn=lambda x: x.show(), count=1, timeout=tiempo)

for packet in pkt_capturado:
    print(packet.show())

# if not pkt_capturado:
#     print("No llego nada") # esto es solo para probar 

# print("IMPRIMO PACKET CAPTURADO")
# pkt_capturado.show()
# print("FIN PACKET CAPTURADO")

