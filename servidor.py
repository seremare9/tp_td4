from scapy.all import *
import canalruidoso as f
from scapy.all import TCP, IP

interface = "lo0" 
# interface = "Software Loopback Interface 1"

listen_port = 8000  

conectado = True # Cuando quiera terminar la conexión lo seteo en False

contador_de_fallas = 0

while conectado and contador_de_fallas < 3:

    print(f"Listening for TCP packets on port {listen_port}...")
    filter_str = f"tcp port {listen_port}"

    pkt_capturado = sniff(iface = interface, count=1, timeout=10) 

    if pkt_capturado: # Si capturó un paquete sin delay

        paquete = pkt_capturado[0]
        flag = paquete[TCP].flags

        flags_esperadas = ("S", "A", "FA")

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
                pass #capaz no haga falta xq ya filtramos antes

    else: # Si pasaron 3 segundos y no recibí ningún paquete
        contador_de_fallas += 1
        continue # Hay que resolverlo, de momento paso a la siguiente iteracion

print("Fin")