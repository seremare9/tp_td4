# En este archivo vamos a definir todas las funciones auxiliares que utilicemos
from scapy.all import raw

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