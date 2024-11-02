import matplotlib.pyplot as plt
import os

# Grafico 1: Paquetes perdidos

eje_x_perdidos = [25, 50, 75, 100] # Paquetes enviados
eje_y_perdidos = [0.12, 0.16, 0.09333, 0.09] # % que se perdieron

# Crear el gráfico
plt.bar(eje_x_perdidos, eje_y_perdidos, color='red', width=15)

# Añadir título y etiquetas
plt.title('Porcentaje de paquetes que se pierden')
plt.xlabel('Cant. de paquetes enviados')
plt.ylabel('Porcentaje de paquetes que se pierden')

plt.xticks(eje_x_perdidos)

# Añadir cuadrícula
plt.grid(True)

# # Guardar gráfico
ruta_grafico = os.path.join('../Gráficos', 'perdidos.png')
plt.savefig(ruta_grafico)

# Mostrar el gráfico
plt.show()


# Grafico 2: Delay

eje_x_delay = [25, 50, 75, 100] # Paquetes enviados
eje_y_delay = [5.015794992446899, 5.016626358032227, 5.013575768470764, 5.014672607183456] # % que se perdieron

# Crear el gráfico
plt.bar(eje_x_delay, eje_y_delay, color='red', width=15)

# Añadir título y etiquetas
plt.title('Delay promedio')
plt.xlabel('Cant. de paquetes enviados')
plt.ylabel('Delay promedio de paquetes retrasados')

plt.xticks(eje_x_delay)

# Añadir cuadrícula
plt.grid(True)

# # Guardar gráfico
ruta_grafico = os.path.join('../Gráficos', 'delay.png')
plt.savefig(ruta_grafico)

# Mostrar el gráfico
plt.show()


# Grafico 3: Peor caso

eje_x_peor = [25, 50, 75, 100] # Paquetes enviados
eje_y_peor = [0.12, 0.16, 0.09333, 0.09] # % que se perdieron

# Crear el gráfico
plt.bar(eje_x_peor, eje_y_peor, color='red', width=15)

# Añadir título y etiquetas
plt.title('Delay en el peor caso')
plt.xlabel('Cant. de paquetes enviados')
plt.ylabel('Tiempo del paquete que más tardó en llagar')

plt.xticks(eje_x_peor)

# Añadir cuadrícula
plt.grid(True)

# # Guardar gráfico
ruta_grafico = os.path.join('../Gráficos', 'peor.png')
plt.savefig(ruta_grafico)

# Mostrar el gráfico
plt.show()


'''
25 paquetes
Cantidad de paquetes enviados: 25
Cantidad de paquetes recibidos: 22
Cantidad de paquetes perdidos: 3
Cantidad de paquetes sin delay: 21
Cantidad de paquetes con delay: 1
Menor delay: 1.0009222030639648
Mayor delay: 5.015794992446899
Delay promedio: 5.015794992446899
Cantidad de paquetes corruptos: 4

50 paquetes
Cantidad de paquetes enviados: 50
Cantidad de paquetes recibidos: 42
Cantidad de paquetes perdidos: 8
Cantidad de paquetes sin delay: 39
Cantidad de paquetes con delay: 3
Menor delay: 1.0074498653411865
Mayor delay: 5.025397300720215
Delay promedio: 5.016626358032227
Cantidad de paquetes corruptos: 4

75 paquetes
Cantidad de paquetes enviados: 75
Cantidad de paquetes recibidos: 68
Cantidad de paquetes perdidos: 7
Cantidad de paquetes sin delay: 58
Cantidad de paquetes con delay: 10
Menor delay: 0.9819598197937012
Mayor delay: 5.022305965423584
Delay promedio: 5.013575768470764
Cantidad de paquetes corruptos: 11

100 paquetes
Cantidad de paquetes enviados: 100
Cantidad de paquetes recibidos: 91
Cantidad de paquetes perdidos: 9
Cantidad de paquetes sin delay: 83
Cantidad de paquetes con delay: 8
Menor delay: 1.0009961128234863
Mayor delay: 5.021087884902954
Delay promedio: 5.014672607183456
Cantidad de paquetes corruptos: 11
'''



'''
25 paquetes
Cantidad de paquetes enviados: 25
Cantidad de paquetes recibidos: 22
Cantidad de paquetes perdidos: 3
Cantidad de paquetes sin delay: 15
Cantidad de paquetes con delay: 7
Cantidad de paquetes corruptos: 1

50 paquetes
Cantidad de paquetes enviados: 50
Cantidad de paquetes recibidos: 44
Cantidad de paquetes perdidos: 6
Cantidad de paquetes sin delay: 34
Cantidad de paquetes con delay: 10
Cantidad de paquetes corruptos: 14

75 paquetes
Cantidad de paquetes enviados: 75
Cantidad de paquetes recibidos: 59
Cantidad de paquetes perdidos: 16
Cantidad de paquetes sin delay: 51
Cantidad de paquetes con delay: 8
Cantidad de paquetes corruptos: 9

100 paquetes
Cantidad de paquetes enviados: 100
Cantidad de paquetes recibidos: 97
Cantidad de paquetes perdidos: 3
Cantidad de paquetes sin delay: 84
Cantidad de paquetes con delay: 13
Cantidad de paquetes corruptos: 11
'''