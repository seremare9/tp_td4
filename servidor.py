from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP

# print(conf.ifaces)

#interface = "lo0" # loopback en Mac, en Windows hay que usar otra (descomentar linea 5 para ver las opciones)
interface = "Software Loopback Interface 1"

listen_port = 8000  

print(f"Listening for TCP packets on port {listen_port}...")
filter_str = f"tcp port {listen_port}"

pkt_capturado = sniff(iface = interface, prn=lambda x: x.show(), timeout=120)

if pkt_capturado:
    for pkt in pkt_capturado:
        paquete = pkt[0]
        flag = paquete[TCP].flags

        # Checksum
        if paquete[IP].chksum == paquete[IP].calc_chksum():
            error_checksum = False # Llego ok
        else:
            error_checksum = True # como procedemos?


        if flag == "S":
            ip = IP(dst=paquete[IP].src, src=paquete[IP].dst)
            tcp = TCP(dport=paquete[TCP].sport, sport=listen_port, seq=10, ack=paquete[TCP].seq+1, flags="SA")
            synack_packet = ip/tcp 
            f.envio_paquetes_inseguro(synack_packet)

        elif flag == "A":
            time.sleep(20)
            ip = IP(dst=paquete[IP].src, src=paquete[IP].dst)
            tcp = TCP(dport=paquete[TCP].sport, sport=listen_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="F")
            fin_packet = ip/tcp 
            f.envio_paquetes_inseguro(fin_packet)

        elif flag == "FA":
            ip = IP(dst=paquete[IP].src, src=paquete[IP].dst)
            tcp = TCP(dport=paquete[TCP].sport, sport=listen_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="A")
            ultimoack_packet = ip/tcp 
            f.envio_paquetes_inseguro(ultimoack_packet)            


#for packet in pkt_capturado:
#    print(packet.show())

# if not pkt_capturado:
#     print("No llego nada") # esto es solo para probar 

# print("IMPRIMO PACKET CAPTURADO")
# pkt_capturado.show()
# print("FIN PACKET CAPTURADO")