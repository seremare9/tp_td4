from cliente import *
from servidor import *
from funcionesAuxiliares import *
from multiprocessing import Process

# interface = "lo0" 
interface = "Software Loopback Interface 1"

# Servidor
def handshake_servidor():
    conectado = True

    ultimo_packet_enviado = "NONE"

    while conectado:

        print(f"Listening for TCP packets on port {listen_port}...")
        filter_str = f"tcp port {listen_port}"

        pkt_capturado = sniff(iface = interface, filter=filter_str, count=1, timeout=3) 

        if pkt_capturado: # Si capturó un paquete sin delay

            paquete = pkt_capturado[0]
            flag = paquete[TCP].flags

            flags_esperadas = ("S", "A", "FA")

            if not(flag in flags_esperadas):
                continue # Paso a la siguiente iteración

            paquete.show()

            if not check_sum(paquete):
                print(f"El paquete con la flag {flag} está corrupto")
                continue # Sigue escuchando

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
                if(ultimo_packet_enviado == "FIN" or ultimo_packet_enviado == "ACK"):
                    ip = IP(dst=paquete[IP].src, src=paquete[IP].dst)
                    tcp = TCP(dport=paquete[TCP].sport, sport=listen_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="A")
                    ultimoack_packet = ip/tcp 
                    ultimo_packet_enviado = "ACK"
                    f.envio_paquetes_inseguro(ultimoack_packet)
        
            else:
                continue 

        else: # Si pasaron 3 segundos y no recibí ningún paquete

            if ultimo_packet_enviado == "NONE": # Me mantengo en LISTEN
                continue
            elif ultimo_packet_enviado == "SYN_ACK": # Retransmito el paquete SYN ACK
                f.envio_paquetes_inseguro(synack_packet)
                
            elif ultimo_packet_enviado == "FIN": # Retransmito el paquete FIN
                f.envio_paquetes_inseguro(fin_packet)

            elif ultimo_packet_enviado == "ACK":
                conectado = False # Termino el while porque voy a cerrar la conexión.

            else: # Paso a la siguiente iteración
                continue
            
    print("Fin de la conexión")

def pseudo_header(ip_src, ip_dst, ip_proto, length):
    """
    Return a pseudo header according to RFC768
    """
    # Prepare the binary representation of the pseudo header
    return struct.pack("!4s4sHH", inet_aton(ip_src), inet_aton(ip_dst), ip_proto, length)

def check_sum(paquete) -> bool:
    # Guardamos el valor del header en una variable
    tcp_checksum = paquete[TCP].chksum
    # Seteamos el valor del header en cero para recalcularlo
    paquete[TCP].chksum = 0
    # Creamos un pseudo header
    ph = pseudo_header(paquete[IP].src, paquete[IP].dst, paquete[IP].proto, len(paquete[TCP]))
    # Calculamos el checksum del contenido del paquete con el pseudo header
    checksum_calculado = checksum(bytes(paquete[TCP]) + ph)

    return tcp_checksum == checksum_calculado




# Cliente

def handshake_cliente():
    retransmisiones_finack = 0 # una herramienta misteriosa que nos ayudará más tarde
    # Asignamos nro de secuencia y de ACK
    ultimo_packet_enviado = "NONE"
    if ultimo_packet_enviado == "NONE":
        num_seq = random.randint(1, 10000) 
        num_ack = 0
        print(num_seq)

        # Armamos el paquete
        ip = IP(dst=dest_ip,src =source_ip)
        tcp = TCP(dport=dest_port, sport =src_port, seq=num_seq, ack=num_ack, flags="S")
        syn_packet = ip/tcp 

        ultimo_packet_enviado = "SYN" # Variable para tener registro de las flags enviadas por el cliente.

        f.envio_paquetes_inseguro(syn_packet) # Se envía el paquete que contiene el SYN.


    conectado = True 

    print(f"Listening for TCP packets on port {src_port}...")
    filter_str = f"tcp port {src_port}"

    while conectado: # Acá manejamos todo lo que pasa después de que se envia el SYN

        print(f"Listening for TCP packets on port {src_port}...")
        filter_str = f"tcp port {src_port}"

        pkt_capturado = sniff(iface = interface, filter=filter_str, count=1, timeout=3) 

        if pkt_capturado: # Si capturó un paquete sin delay

            print(pkt_capturado)

            paquete = pkt_capturado[0]

            flag = paquete[TCP].flags

            flags_esperadas = ("SA", "A", "F")

            if not(flag in flags_esperadas):
                continue # Paso a la siguiente iteración

            pkt_capturado[0].show()

            if not check_sum(paquete):
                print(f"El paquete con la flag {flag} está corrupto")
                continue # Sigue escuchando
                

            if flag == "SA": # Si recibe un SYN+ACK, manda un ACK
                ip = IP(dst=dest_ip,src =source_ip)
                tcp = TCP(dport=dest_port, sport =src_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="A")
                ack_packet = ip/tcp 
                ultimo_packet_enviado = "ACK"
                f.envio_paquetes_inseguro(ack_packet) # Se envía el paquete que contiene el ACK
                time.sleep(20) # Espera los 20 segundos que se toma el servidor en mandar el FIN

            elif flag == "F":
                ip = IP(dst=dest_ip,src =source_ip)
                tcp = TCP(dport=dest_port, sport =src_port, seq=paquete[TCP].ack, ack=paquete[TCP].seq+1, flags="FA")
                finack_packet = ip/tcp 
                ultimo_packet_enviado = "FIN_ACK"
                f.envio_paquetes_inseguro(finack_packet) # Se envía el paquete que contiene el FIN+ACK 

            elif flag == "A": # Recibe el último ACK. Ya se puede cerrar la conexión
                    conectado = False
                    
            else:
                continue 
                    
        else: # Si pasaron 3 segundos y no recibí ningún paquete
            
            if ultimo_packet_enviado == "SYN": # Retransmito el paquete SYN
                f.envio_paquetes_inseguro(syn_packet)
                
            elif ultimo_packet_enviado == "ACK": # Retransmito el paquete ACK
                f.envio_paquetes_inseguro(ack_packet)

            elif ultimo_packet_enviado == "FIN_ACK":
                '''
                El cliente retransmitirá el FIN ACK varias veces. Si después de un número determinado de retransmisiones 
                aún no recibe el ACK, el cliente terminará cerrando la conexión de manera unilateral, agotando su temporizador.
                '''
                if retransmisiones_finack < 5: # Se asume que el servidor cerró la conexión
                    f.envio_paquetes_inseguro(finack_packet)
                    retransmisiones_finack += 1
                else:
                    conectado = False # Cierro la conexión
                    
            else: # Paso a la siguiente iteración
                continue

    print("Fin de la conexión")




# Test

if __name__ == '__main__':
    p1 = Process(target=handshake_servidor)
    p2 = Process(target=handshake_cliente)
    p1.start()
    p2.start()
