# En este archivo vamos a definir todas las funciones auxiliares que utilicemos
from scapy.all import raw
from scapy.all import *
import struct

def checksum_manual(packet):
    data = raw(packet)
    # Convertir en palabras de 16 bits y sumar
    total_sum = sum(int.from_bytes(data[i:i+2], 'big') for i in range(0, len(data), 2))
    
    # Agregar el carry si es mayor de 16 bits
    while (total_sum >> 16) > 0:
        total_sum = (total_sum & 0xFFFF) + (total_sum >> 16)
        
    # Tomar el complemento de 16 bits
    checksum = ~total_sum & 0xFFFF
    return checksum


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