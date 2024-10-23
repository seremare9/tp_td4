from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP

#interface = "lo0" 
interface = "Software Loopback Interface 1"

listen_port = 8000  

conectado = True # Cuando quiera terminar la conexión lo seteo en False

while conectado:

    print(f"Listening for TCP packets on port {listen_port}...")
    filter_str = f"tcp port {listen_port}"

    pkt_capturado = sniff(iface = interface, prn=lambda x: x.show(), count=1, timeout=3) 

    if pkt_capturado: # Si capturó un paquete sin delay

        paquete = pkt_capturado[0]
        flag = paquete[TCP].flags

        # Checksum
        if paquete[IP].chksum != paquete[IP].calc_chksum() or paquete[TCP].chksum != paquete[TCP].calc_chksum():
            # El paquete llego corrupto y hay que retransmitir
            None # Esto lo voy a borrar despues
        
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
                # Habría que ver que pasa si el cliente no recibe este ACK...

        # # Hay que definir que hacer si llega un paquete con otra flag. Jaime dijo que lo ignoremos
            