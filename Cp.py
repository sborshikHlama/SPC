import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def calculate_cp(usl, lsl, data):
	std = np.std(data, ddof=1)
	Cp = (usl - lsl) / (6 * std)
	return Cp

file_path = 'kpis_ordered.csv'
data = pd.read_csv(file_path)
germany_data = data[data["Country"] == "Germany"]
print(germany_data.head())
FCR = germany_data["First_Contact_Resolution"]
ART = germany_data["Average_Resolution_Time"]
cp_fcr = calculate_cp(80, 75, FCR)
cp_art = calculate_cp(8.7, 2, ART)
print("Cp FCR: ", cp_fcr)
print("Cp ART: ", cp_art)

