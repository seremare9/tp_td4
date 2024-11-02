import matplotlib.pyplot as plt

# Grafico 1: Paquetes perdidos

eje_x_perdidos = [] # Paquetes enviados
eje_y_perdidos = [] # % que se perdieron

# Crear el gráfico
plt.plot(eje_x_perdidos, eje_y_perdidos, color='red', linestyle='-', marker='o')

# Añadir título y etiquetas
plt.title('Porcentaje de paquetes que se pierden')
plt.xlabel('Cant. de paquetes enviados')
plt.ylabel('Porcentaje de paquetes que se pierden')

# Añadir cuadrícula
plt.grid(True)

# # Guardar gráfico
# plt.savefig('grafico_ejemplo.png')

# Mostrar el gráfico
plt.show()