# En este archivo vamos a definir todas las funciones auxiliares que utilicemos

def calc_checksum(packet):
    # Si la longitud del paquete no es par, agregar un byte nulo al final
    if len(packet) % 2 == 1:
        packet += b'\x00'
    
    # Dividir el paquete en segmentos de 16 bits y sumar
    checksum = 0
    for i in range(0, len(packet), 2):
        word = (packet[i] << 8) + packet[i + 1]  # Juntar dos bytes para hacer un "word"
        checksum += word

    # Agregar los acarreos (carry) al final
    checksum = (checksum >> 16) + (checksum & 0xffff)  # Sumar los acarreos
    checksum += (checksum >> 16)  # Si hay otro carry

    # Tomar el complemento a uno y devolver como resultado
    return ~checksum & 0xffff

# Ejemplo de uso con un paquete Scapy
from scapy.all import IP, TCP

# Crear un paquete TCP/IP con Scapy
packet = IP(dst="192.168.1.1")/TCP(dport=80)

# Calcular el checksum manualmente
ip_payload = bytes(packet[IP])  # Obtener el payload del paquete IP como bytes
tcp_payload = bytes(packet[TCP])  # Obtener el payload del paquete TCP como bytes

ip_checksum = calc_checksum(ip_payload)
tcp_checksum = calc_checksum(tcp_payload)

print(f"Checksum IP: {hex(ip_checksum)}")
print(f"Checksum TCP: {hex(tcp_checksum)}")