import matplotlib.pyplot as plt
import numpy as np
# Data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import kagglehub
import os

# Load and prepare data
path = kagglehub.dataset_download("drnimishadavis/call-center-performance-data")
files = os.listdir(path)
filename = next(f for f in files if f.endswith(".xlsx"))
ful_path = os.path.join(path, filename)
df_calls = pd.read_excel(ful_path)

df_answered = df_calls[df_calls['Answered (Y/N)'] == 'Y']
df_answered['Date'] = pd.to_datetime(df_answered['Date'])
df_answered = df_answered.sort_values(by='Date')
df_answered = df_answered[['Date', 'Resolved']]

# Define subgroups
subgroup_size = 50
num_subgroups = len(df_answered) // subgroup_size
subgroups = [df_answered.iloc[i * subgroup_size:(i + 1) * subgroup_size] for i in range(num_subgroups)]

# Calculate defectives and proportions
defectives = [subgroup['Resolved'].value_counts().get('N', 0) for subgroup in subgroups]
for d in defectives:
	print(d)
proportions = [d / subgroup_size for d in defectives]

# Calculate control limits
p_bar = np.mean(proportions)
np_bar = p_bar * subgroup_size
ucl_np = np_bar + 3 * np.sqrt(np_bar * (1 - p_bar))
lcl_np = max(np_bar - 3 * np.sqrt(np_bar * (1 - p_bar)), 0)
ucl_p = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / subgroup_size)
lcl_p = max(p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / subgroup_size), 0)

# Plot NP-chart
plt.figure(figsize=(12, 6))
plt.plot(defectives, marker='o', linestyle='-', color='b', label='Defectives')
plt.axhline(np_bar, color='g', linestyle='--', label=f'CL = {np_bar:.2f}')
plt.axhline(ucl_np, color='r', linestyle='--', label=f'UCL = {ucl_np:.2f}')
plt.axhline(lcl_np, color='r', linestyle='--', label=f'LCL = {lcl_np:.2f}')
plt.title('NP-Chart: Number of Unresolved Calls per Subgroup')
plt.xlabel('Subgroup')
plt.ylabel('Number of Unresolved Calls')
plt.legend()
plt.grid(True)
plt.savefig('p_chart.png')
plt.show()

# Plot P-chart
plt.figure(figsize=(12, 6))
plt.plot(proportions, marker='o', linestyle='-', color='b', label='Proportion')
plt.axhline(p_bar, color='g', linestyle='--', label=f'CL = {p_bar:.3f}')
plt.axhline(ucl_p, color='r', linestyle='--', label=f'UCL = {ucl_p:.3f}')
plt.axhline(lcl_p, color='r', linestyle='--', label=f'LCL = {lcl_p:.3f}')
plt.title('P-Chart: Proportion of Unresolved Calls per Subgroup')
plt.xlabel('Subgroup')
plt.ylabel('Proportion of Unresolved Calls')
plt.legend()
plt.grid(True)
plt.savefig('np_chart.png')
plt.show()