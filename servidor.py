from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP

#interface = "lo0" 
interface = "Software Loopback Interface 1"

listen_port = 8000  

conectado = True # Cuando quiera terminar la conexión lo seteo en False

def mostrar_flags(pkt): # Función auxiliar que voy a usar para mostrar los paquetes capturados
    if TCP in pkt:
        flags = pkt[TCP].flags
        # Verificar si las flags son SYN+ACK (0x12), ACK (0x10) o FIN+ACK (0x11)
        if flags & 0x12 == 0x12 or flags & 0x10 == 0x10 or flags & 0x11 == 0x11:
            pkt.show()

while conectado:

    print(f"Listening for TCP packets on port {listen_port}...")
    filter_str = f"tcp port {listen_port}"

    pkt_capturado = sniff(iface = interface, prn=mostrar_flags, count=1, timeout=3) 

    if pkt_capturado: # Si capturó un paquete sin delay

        paquete = pkt_capturado[0]
        flag = paquete[TCP].flags

        # Checksum
        if paquete[IP].chksum != paquete[IP].calc_chksum() or paquete[TCP].chksum != paquete[TCP].calc_chksum():
            # El paquete llego corrupto y hay que retransmitir
            pass # Esto lo voy a borrar despues
        
        else: # Si el paquete que recibí no está corrupto, mando la respuesta al cliente
    
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

                conectado = False # Termino el while porque voy a cerrar la conexión. 
     
            else:
                pass

    else: # Si pasaron 3 segundos y no recibí ningún paquete
        pass # Hay que resolverlo
            