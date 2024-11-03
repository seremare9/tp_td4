from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP
from checksum import *

interface = "Software Loopback Interface 1"

listen_port = 8000  

conectado = True

ultimo_packet_enviado = "NONE" # Variable para tener registro de las flags enviadas por el servidor

while conectado:

    print(f"Listening for TCP packets on port {listen_port}...")
    filter_str = f"tcp port {listen_port}"

    pkt_capturado = sniff(iface = interface, filter=filter_str, count=1, timeout=3) 

    if pkt_capturado: # Si capturó un paquete sin delay

        paquete = pkt_capturado[0]

        # Se fija que las flags del paquete sean las correspondientes al handshake y/o al cierre
        flag = paquete[TCP].flags

        flags_esperadas = ("S", "A", "FA")

        if not(flag in flags_esperadas):
            continue # Pasa a la siguiente iteración

        paquete.show()

        # Checksum
        tcp_checksum = paquete[TCP].chksum

        print(f"Checksum TCP del paquete con la flag {flag}: {tcp_checksum}")

        paquete[TCP].chksum = 0
        ph = pseudo_header(paquete[IP].src, paquete[IP].dst, paquete[IP].proto, len(paquete[TCP])) # Arma un pseudo header con los datos del paquete
        checksum_calculado = checksum(bytes(paquete[TCP]) + ph) # Recalcula el checksum usando el pseudo header y los bytes del paquete TCP
        print(f"Checksum calculado del paquete con la flag {flag}: {checksum_calculado}")

        if tcp_checksum != checksum_calculado:
            print(f"El paquete con la flag {flag} está corrupto")
            continue # Sigue escuchando

        if flag == "S": # Recibe un SYN
            ip = IP(dst=paquete[IP].src, src=paquete[IP].dst)
            tcp = TCP(dport=paquete[TCP].sport, sport=listen_port, seq=10, ack=paquete[TCP].seq+1, flags="SA")
            synack_packet = ip/tcp 
            ultimo_packet_enviado = "SYN_ACK"
            f.envio_paquetes_inseguro(synack_packet) # Envía el paquete que contiene el SYN+ACK

        elif flag == "A": # Recibe un ACK
            time.sleep(20) # Espera 20 segundos para mandar el FIN
            ip = IP(dst=paquete[IP].src, src=paquete[IP].dst)
            tcp = TCP(dport=paquete[TCP].sport, sport=listen_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="F")            
            fin_packet = ip/tcp 
            ultimo_packet_enviado = "FIN"
            f.envio_paquetes_inseguro(fin_packet) # Envía el paquete que contiene el FIN

        elif flag == "FA": # Recibe un FIN+ACK
            if(ultimo_packet_enviado == "FIN" or ultimo_packet_enviado == "ACK"):
                ip = IP(dst=paquete[IP].src, src=paquete[IP].dst)
                tcp = TCP(dport=paquete[TCP].sport, sport=listen_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="A")
                ultimoack_packet = ip/tcp 
                ultimo_packet_enviado = "ACK"
                f.envio_paquetes_inseguro(ultimoack_packet) # Envía el paquete que contiene el último ACK
     
        else: # Vuelve a escuchar
            continue 

    else: # Si pasaron 3 segundos y no recibió ningún paquete

        if ultimo_packet_enviado == "NONE": # Se mantiene en LISTEN
            continue
        elif ultimo_packet_enviado == "SYN_ACK": # Retransmite el paquete SYN+ACK
            f.envio_paquetes_inseguro(synack_packet)
            
        elif ultimo_packet_enviado == "FIN": # Retransmite el paquete FIN
            f.envio_paquetes_inseguro(fin_packet)

        elif ultimo_packet_enviado == "ACK":
            conectado = False # Termina el ciclo y cierra la conexión

        else: # Vuelve a escuchar
            continue

print("Fin de la conexión")