from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP
from funcionesAuxiliares import *

# interface = "lo0" 
interface = "Software Loopback Interface 1"

listen_port = 8000  

conectado = True

ultimo_packet_enviado = "NONE"

while conectado:

    print(f"Listening for TCP packets on port {listen_port}...")
    filter_str = f"tcp port {listen_port}"

    pkt_capturado = sniff(iface = interface, filter=filter_str, count=1, timeout=10) 

    if pkt_capturado: # Si capturó un paquete sin delay

        paquete = pkt_capturado[0]
        flag = paquete[TCP].flags

        flags_esperadas = ("S", "A", "FA")

        if not(flag in flags_esperadas):
            continue # Paso a la siguiente iteración

        paquete.show()

        # Checksum
        '''

        # ip_checksum = paquete[IP].chksum
        tcp_checksum = paquete[TCP].chksum

        #print(f"Checksum IP del paquete con la flag {flag}: {ip_checksum}")
        print(f"Checksum TCP del paquete con la flag {flag}: {tcp_checksum}")
        
        paquete[TCP].chksum = None

        # Recalculamos el checksum del paquete recibido
        bytes_tcp = bytes(paquete[TCP])

        print(calc_checksum(bytes_tcp))


        #if ip_checksum != 0 or tcp_checksum != 0:
            #print(f"El paquete con la flag {flag} está corrupto")
            # Tengo que retransmitir
            #contador_de_fallas += 1
            #continue

        if tcp_checksum != calc_checksum(bytes_tcp):
            print("El paquete está corrupto")
        else: # Si el paquete que recibí no está corrupto, mando la respuesta al cliente
        '''

        if flag == "S":
            ip = IP(dst=paquete[IP].src, src=paquete[IP].dst)
            tcp = TCP(dport=paquete[TCP].sport, sport=listen_port, seq=10, ack=paquete[TCP].seq+1, flags="SA")
            synack_packet = ip/tcp 
            ultimo_packet_enviado = "SYN_ACK"
            f.envio_paquetes_inseguro(synack_packet)

        elif flag == "A":
            time.sleep(20)
            ip = IP(dst=paquete[IP].src, src=paquete[IP].dst)
            tcp = TCP(dport=paquete[TCP].sport, sport=listen_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="F")            
            fin_packet = ip/tcp 
            ultimo_packet_enviado = "FIN"
            f.envio_paquetes_inseguro(fin_packet)

        elif flag == "FA":
            ip = IP(dst=paquete[IP].src, src=paquete[IP].dst)
            tcp = TCP(dport=paquete[TCP].sport, sport=listen_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="A")
            ultimoack_packet = ip/tcp 
            ultimo_packet_enviado = "ACK"
            f.envio_paquetes_inseguro(ultimoack_packet)

            conectado = False # Termino el while porque voy a cerrar la conexión.
     
        else:
            continue 

    else: # Si pasaron 3 segundos y no recibí ningún paquete

        if ultimo_packet_enviado == "NONE": # Me mantengo en LISTEN
            continue
        elif ultimo_packet_enviado == "SYN_ACK": # Retransmito el paquete SYN ACK
            f.envio_paquetes_inseguro(synack_packet)
            
        elif ultimo_packet_enviado == "FIN": # Retransmito el paquete FIN
            f.envio_paquetes_inseguro(fin_packet)

        elif ultimo_packet_enviado == "ACK": # Retransmito el paquete ACK
            f.envio_paquetes_inseguro(ultimoack_packet)

        else: # Paso a la siguiente iteración
            continue

        

print("Fin de la conexión")