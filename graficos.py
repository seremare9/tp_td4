import matplotlib.pyplot as plt
import os

# Grafico 1: Paquetes perdidos

eje_x_perdidos = [25, 50, 75, 100, 125, 150, 175, 200] # Paquetes enviados
eje_y_perdidos = [0.12, 0.16, 0.09333, 0.09, 0.104, 0.07333, 0.0571, 0.105] # Proporciones de paquetes que se perdieron (valores calculados a mano)

# Crear el gráfico
plt.bar(eje_x_perdidos, eje_y_perdidos, color='red', width=15)

plt.title('Proporción de packet loss')
plt.xlabel('Cant. de paquetes enviados')
plt.ylabel('Proporción de paquetes que se pierden')

plt.xticks(eje_x_perdidos)

plt.grid(axis='y')

# Guardar gráfico
ruta_grafico = os.path.join('../Gráficos', 'perdidos.png')
plt.savefig(ruta_grafico)

# Mostrar el gráfico
plt.show()


# Grafico 2: Delay

eje_x_delay = [25, 50, 75, 100, 125, 150, 175, 200] # Paquetes enviados
eje_y_delay = [5.015794992446899, 5.016626358032227, 5.013575768470764, 5.014672607183456, 5.014866267933565, 5.013048073824714, 5.0172685543696085, 5.017916287694659] # Delay promedio en cada caso

# Crear el gráfico
plt.plot(eje_x_delay, eje_y_delay, color='purple')

plt.title('Delay promedio')
plt.xlabel('Cant. de paquetes enviados')
plt.ylabel('Delay promedio de paquetes retrasados')

plt.xticks(eje_x_delay)
plt.ylim(5.0, 5.03)

plt.grid(True)

# Guardar gráfico
ruta_grafico = os.path.join('../Gráficos', 'delay.png')
plt.savefig(ruta_grafico)

# Mostrar el gráfico
plt.show()


# Grafico 3: Peor caso

eje_x_peor = [25, 50, 75, 100, 125, 150, 175, 200] # Paquetes enviados
eje_y_peor = [5.015794992446899, 5.025397300720215, 5.022305965423584, 5.021087884902954, 5.028006076812744, 5.02164888381958, 5.0934436321258545, 5.195056200027466] # Delay del paquete que más tardó en llegar en cada caso

# Crear el gráfico
plt.scatter(eje_x_peor, eje_y_peor, color='blue', s=40)

plt.title('Delay en el peor caso')
plt.xlabel('Cant. de paquetes enviados')
plt.ylabel('Tiempo del paquete que más tardó en llegar')

plt.xticks(eje_x_peor)
plt.ylim(4, 6)

plt.grid(True)

# Guardar gráfico
ruta_grafico = os.path.join('../Gráficos', 'peor.png')
plt.savefig(ruta_grafico)

# Mostrar el gráfico
plt.show()


# Grafico 4: Paquetes corruptos

eje_x_corrupto = [25, 50, 75, 100, 125, 150, 175, 200] # Paquetes enviados
eje_y_corrupto = [0.18, 0.095, 0.16, 0.1208, 0.0892, 0.1223, 0.09, 0.0837] # Proporciones de paquetes corruptos (valores calculados a mano)

# Crear el gráfico
plt.bar(eje_x_corrupto, eje_y_corrupto, color='green', width=15)

plt.title('Corrupción de paquetes')
plt.xlabel('Cant. de paquetes enviados')
plt.ylabel('Proporción de paquetes corruptos que llegaron')

plt.xticks(eje_x_corrupto)

plt.grid(axis='y')

# Guardar gráfico
ruta_grafico = os.path.join('../Gráficos', 'corrupcion.png')
plt.savefig(ruta_grafico)

# Mostrar el gráfico
plt.show()


# Gráfico 5: Paquetes con delay

eje_x_peor = [25, 50, 75, 100, 125, 150, 175, 200] # Paquetes enviados
eje_y_peor = [0.045, 0.0714, 0.147, 0.0879, 0.1517, 0.1223, 0.18, 0.156] # Proporciones de paquetes que llegaron con delay (valores calculados a mano)

# Crear el gráfico
plt.scatter(eje_x_peor, eje_y_peor, color='orange', s=40)

plt.title('Paquetes con delay')
plt.xlabel('Cant. de paquetes enviados')
plt.ylabel('Proporción de paquetes que llegan con delay')

plt.xticks(eje_x_peor)

plt.grid(True)

# Guardar gráfico
ruta_grafico = os.path.join('../Gráficos', 'proporcion_delay.png')
plt.savefig(ruta_grafico)

# Mostrar el gráfico
plt.show()


'''
Resultado de los tests:

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

125 paquetes
Cantidad de paquetes enviados: 125
Cantidad de paquetes recibidos: 112
Cantidad de paquetes perdidos: 13
Cantidad de paquetes sin delay: 95
Cantidad de paquetes con delay: 17
Menor delay: 0.99747633934021
Mayor delay: 5.028006076812744
Delay promedio: 5.014866267933565
Cantidad de paquetes corruptos: 10

150 paquetes
Cantidad de paquetes enviados: 150
Cantidad de paquetes recibidos: 139
Cantidad de paquetes perdidos: 11
Cantidad de paquetes sin delay: 122
Cantidad de paquetes con delay: 17
Menor delay: 1.0032124519348145
Mayor delay: 5.02164888381958
Delay promedio: 5.013048073824714
Cantidad de paquetes corruptos: 17

175 paquetes
Cantidad de paquetes enviados: 175
Cantidad de paquetes recibidos: 165
Cantidad de paquetes perdidos: 10
Cantidad de paquetes sin delay: 135
Cantidad de paquetes con delay: 30
Menor delay: 0.9960291385650635
Mayor delay: 5.0934436321258545
Delay promedio: 5.0172685543696085
Cantidad de paquetes corruptos: 15

200 paquetes
Cantidad de paquetes enviados: 200
Cantidad de paquetes recibidos: 179
Cantidad de paquetes perdidos: 21
Cantidad de paquetes sin delay: 151
Cantidad de paquetes con delay: 28
Menor delay: 1.0026180744171143
Mayor delay: 5.195056200027466
Delay promedio: 5.017916287694659
Cantidad de paquetes corruptos: 15
'''