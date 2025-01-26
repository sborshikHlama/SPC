import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

constanta = 0.3

temp = [85, 80, 90, 88, 92, 85, 87, 86, 93, 75, 80, 88, 84, 86, 89]  
ewma_values = []
point = 0

for t in temp:
	point = constanta * point + ((1 - constanta) * t)
	print(point) 
	ewma_values.append(point)

x_coordinates = list(range(1, len(temp) + 1))
plt.scatter(x_coordinates, temp)
plt.plot(x_coordinates, ewma_values, 'b-', label='EWMA')
plt.xlabel('Days')
plt.ylabel('FCR')
plt.title('FCR and EWMA Over Days')
plt.legend()
plt.savefig('EWMA.png')
