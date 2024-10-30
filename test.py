from cliente import *
from servidor import *
from funcionesAuxiliares import *

cliente_conectado = True
servidor_conectado = True
conexion_abierta = True

while conexion_abierta:
    # El cliente evía el paquete con el SYN
    enviar_syn()

    # Cliente
    while cliente_conectado:
        # Acá va/n funcion/es con la que recibe y envía paquetes el cliente
        servidor_conectado = True
        break

    # Servidor
    while servidor_conectado:
        # Acá va/n funcion/es con la que recibe y envía paquetes el cliente
        break