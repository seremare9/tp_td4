import canalruidoso as f 
from scapy.all import * 
from scapy.all import TCP, IP
import time
import random
from checksum import *

retransmisiones_finack = 0 # Se declara afuera del ciclo para usarla en caso de tener que retransmitir el último paquete

# Parámetros
source_ip = '127.0.0.1'
dest_ip = '127.0.0.1'
dest_port = 8000
src_port = 5000
num_seq = random.randint(1, 10000) 
num_ack = 0

# Arma el paquete
ip = IP(dst=dest_ip,src =source_ip)
tcp = TCP(dport=dest_port, sport =src_port, seq=num_seq, ack=num_ack, flags="S")
syn_packet = ip/tcp 

ultimo_packet_enviado = "SYN" # Variable para tener registro de las flags enviadas por el servidor

f.envio_paquetes_inseguro(syn_packet) # Envía el paquete que contiene el SYN

interface = "Software Loopback Interface 1" 

conectado = True 

print(f"Listening for TCP packets on port {src_port}...")
filter_str = f"tcp port {src_port}"

while conectado: # Todo lo que pasa después de que se envia el SYN

    print(f"Listening for TCP packets on port {src_port}...")
    filter_str = f"tcp port {src_port}"

    pkt_capturado = sniff(iface = interface, filter=filter_str, count=1, timeout=3) 

    if pkt_capturado: # Si capturó un paquete sin delay

        print(pkt_capturado)

        paquete = pkt_capturado[0]
        
        # Se fija que las flags del paquete sean las correspondientes al handshake y/o al cierre
        flag = paquete[TCP].flags

        flags_esperadas = ("SA", "A", "F") 

        if not(flag in flags_esperadas): 
            continue # Pasa a la siguiente iteración

        pkt_capturado[0].show()

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
        

        if flag == "SA": # Recibe un SYN+ACK
            ip = IP(dst=dest_ip,src =source_ip)
            tcp = TCP(dport=dest_port, sport =src_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="A")
            ack_packet = ip/tcp 
            ultimo_packet_enviado = "ACK"
            f.envio_paquetes_inseguro(ack_packet) # Envía el paquete que contiene el ACK
            time.sleep(20) # Espera los 20 segundos que se toma el servidor en mandar el FIN

        elif flag == "F": # Recibe un FIN
            ip = IP(dst=dest_ip,src =source_ip)
            tcp = TCP(dport=dest_port, sport =src_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="FA")
            finack_packet = ip/tcp 
            ultimo_packet_enviado = "FIN_ACK"
            f.envio_paquetes_inseguro(finack_packet) # Envía el paquete que contiene el FIN+ACK 

        elif flag == "A": # Recibe el último ACK del servidor
            conectado = False # Cierra su lado de la conexión
            
        else: # Vuelve a escuchar
            continue 
                
    else: # Si pasaron 3 segundos y no recibió ningún paquete
        
        if ultimo_packet_enviado == "SYN": # Retransmite el paquete SYN
            f.envio_paquetes_inseguro(syn_packet)
            
        elif ultimo_packet_enviado == "ACK": # Retransmite el paquete ACK
            f.envio_paquetes_inseguro(ack_packet)

        elif ultimo_packet_enviado == "FIN_ACK": # El cliente puede retransmitir el FIN+ACK hasta 4 veces y no recibir el ACK del servior
            if retransmisiones_finack < 5: 
                f.envio_paquetes_inseguro(finack_packet)
                retransmisiones_finack += 1
            else:
                conectado = False # Asume que el servidor cerró la conexión y cierra la conexión
                
        else: # Vuelve a escuchar
            continue    
    
print("Fin de la conexión")