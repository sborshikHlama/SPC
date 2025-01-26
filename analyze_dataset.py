import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'cx_kpi.csv'
data = pd.read_csv(file_path)

FCR = data['FCR']

mean_value = FCR.mean()
median_value = FCR.median()
std_dev = FCR.std()
print(f"Mean: {mean_value}, Median: {median_value}, Std Dev: {std_dev}")

sns.histplot(data['ART'], kde=True)
plt.title("Responce time Distribution")
plt.show()

# sns.boxplot(x=data['FCR'])
# plt.show()