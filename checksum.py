from scapy.all import *
import struct

# Función auxiliar para calcular el pseudo header de un paquete recibido, utilizada para calcular el checksum manualmente
def pseudo_header(ip_src, ip_dst, ip_proto, length):
    '''
    Devuelve un pseudo header de acuerdo con RFC768.
    '''
    # Representación binaria del pseudo header con los valores del paquete recibido
    return struct.pack("!4s4sHH", inet_aton(ip_src), inet_aton(ip_dst), ip_proto, length)