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

f.envio_paquetes_inseguro(syn_packet) # Se envía el paquete que contiene el SYN.

# interface = "Software Loopback Interface 1" 
interface = "lo0"

listen_port = 5000  

conectado = True # Cuando quiera terminar la conexión lo seteo en False

while conectado: # Acá manejamos todo lo que pasa después de que se envia el SYN
    '''
    Idea del while: Luego de enviar un paquete SYN ACK o FIN, repito el while para escuchar el siguiente paquete.
    '''

    print(f"Listening for TCP packets on port {listen_port}...")
    filter_str = f"tcp port {listen_port}"

    pkt_capturado = sniff(iface = interface, count=1, timeout=10) 

    contador_de_fallas = 0 # para que no loopee infinitas veces

    if pkt_capturado and contador_de_fallas < 3: # Si capturó un paquete sin delay

        paquete = pkt_capturado[0]

        flag = paquete[TCP].flags

        flags_esperadas = ("SA", "A", "F")

        if not(flag in flags_esperadas):
            contador_de_fallas += 1
            continue # Paso a la siguiente iteración

        pkt_capturado.show()

        # Checksum
        ip_checksum = paquete[IP].chksum
        tcp_checksum = paquete[TCP].chksum

        print(f"Checksum IP del paquete con la flag {flag}: {ip_checksum}")
        print(f"Checksum TCP del paquete con la flag {flag}: {tcp_checksum}")

        if ip_checksum != 0 or tcp_checksum != 0:
            print(f"El paquete con la flag {flag} está corrupto")
            # Tengo que retransmitir
            contador_de_fallas += 1
            continue 

        
        else: # Si el paquete que recibí no está corrupto, mando la respuesta al cliente

            if flag == "SA": # Si recibe un SYN+ACK, manda un ACK
                ip = IP(dst=dest_ip,src =source_ip)
                tcp = TCP(dport=dest_port, sport =src_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="A")
                ack_packet = ip/tcp 
                f.envio_paquetes_inseguro(ack_packet) # Se envía el paquete que contiene el ACK

            elif flag == "F":
                ip = IP(dst=dest_ip,src =source_ip)
                tcp = TCP(dport=dest_port, sport =src_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="FA")
                finack_packet = ip/tcp 
                f.envio_paquetes_inseguro(finack_packet) # Se envía el paquete que contiene el FIN+ACK 

            elif flag == "A": # Recibe el último ACK. Ya se puede cerrar la conexión
                conectado = False
            
            else:
                pass # Ignoro el paquete, capaz no haga falta xq ya filtramos antes
                
    else: # Si pasaron 3 segundos y no recibí ningún paquete
        contador_de_fallas += 1
        continue # Habría que ver como lo resolvemos (volvemos a enviar el paquete anterior?)
        
    
print("Fin")
            
   




















