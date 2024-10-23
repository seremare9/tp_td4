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

interface = "Software Loopback Interface 1" 
# interface = "lo0"

listen_port = 5000  

conectado = True # Cuando quiera terminar la conexión lo seteo en False

def mostrar_flags(pkt): # Función auxiliar que voy a usar para mostrar los paquetes capturados
    if TCP in pkt:
        flags = pkt[TCP].flags
        if flags & 0x12 == 0x12 or flags & 0x01 == 0x01 or flags & 0x10 == 0x10:
            pkt.show()

while conectado: # Acá manejamos todo lo que pasa después de que se envia el SYN
    '''
    Idea del while: Luego de enviar un paquete SYN ACK o FIN, repito el while para escuchar el siguiente paquete.
    '''

    print(f"Listening for TCP packets on port {listen_port}...")
    filter_str = f"tcp port {listen_port}"

    pkt_capturado = sniff(iface = interface, prn=mostrar_flags, count=1, timeout=3) 

    if pkt_capturado: # Si capturó un paquete sin delay

        paquete = pkt_capturado[0]

        flag = paquete[TCP].flags

        # Checksum
        if paquete[IP].chksum != paquete[IP].calc_chksum() or paquete[TCP].chksum != paquete[TCP].calc_chksum():
            # En la slide dice que hay que computar el checksum y comprobar que todos los bits sean 0 (si no lo son hay error)
            # El paquete llego corrupto y hay que retransmitir
            pass # Esto lo voy a borrar despues
        
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
                pass # Ignoro el paquete
                
    else: # Si pasaron 3 segundos y no recibí ningún paquete

        pass # Habría que ver como lo resolvemos (volvemos a enviar el paquete anterior?)
        
    

            
   




















