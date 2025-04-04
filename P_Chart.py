import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import kagglehub
import os

# Download latest version
path = kagglehub.dataset_download("satvicoder/call-center-data")

files = os.listdir(path)


filename = next(f for f in files if f.endswith(".csv"))
ful_path = os.path.join(path, filename)
df = pd.read_csv(ful_path)
sample_df = df.head(60).copy()

sample_df['Incoming Calls'] = pd.to_numeric(sample_df['Incoming Calls'], errors='coerce')
sample_df['Answered Calls'] = pd.to_numeric(sample_df['Answered Calls'], errors='coerce')

sample_df['p'] = sample_df['Answered Calls'] / sample_df['Incoming Calls']

p_bar = sample_df['Answered Calls'].sum() / sample_df['Incoming Calls'].sum()

sample_df['UCL'] = p_bar + 3 * np.sqrt((p_bar * (1 - p_bar)) / sample_df['Incoming Calls'])
sample_df['LCL'] = p_bar - 3 * np.sqrt((p_bar * (1 - p_bar)) / sample_df['Incoming Calls'])
sample_df['LCL'] = sample_df['LCL'].clip(lower=0) 

sample_df['UCL'] = sample_df['UCL'].round(4)
sample_df['LCL'] = sample_df['LCL'].round(4)

plt.figure(figsize=(14, 6))
plt.plot(sample_df.index + 1, sample_df['p'], marker='o', label=' Answer Rate (p)')
plt.step(sample_df.index + 1, sample_df['UCL'], linestyle='--', color='red', label='Upper Limit (UCL)')
plt.step(sample_df.index + 1, sample_df['LCL'], linestyle='--', color='green', label='Lower Limit (LCL)')
plt.axhline(y=p_bar, color='gray', linestyle='-', label='Mean (p)')
plt.title('P-chart Succes answer rate')
plt.xlabel('Day')
plt.ylabel('Answer Rate')
# plt.xticks(ticks=range(1, len(sample_df) + 1))
y_min = min(sample_df['LCL'].min(), sample_df['p'].min()) - 0.01
y_max = max(sample_df['UCL'].max(), sample_df['p'].max()) + 0.01
plt.ylim(y_min, y_max)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()