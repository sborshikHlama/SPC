import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import kagglehub
import os

path = kagglehub.dataset_download("satvicoder/call-center-data")

files = os.listdir(path)
filename = next(f for f in files if f.endswith(".csv"))
ful_path = os.path.join(path, filename)
df = pd.read_csv(ful_path)
cusum_df = df.head(60).copy()
cusum_df['Answer Speed (Seconds)'] = pd.to_timedelta(cusum_df['Answer Speed (AVG)']).dt.total_seconds()
cusum_df = cusum_df.dropna(subset=['Answer Speed (Seconds)'])

target = cusum_df['Answer Speed (Seconds)'].mean()
sigma = cusum_df['Answer Speed (Seconds)'].std()
k = 0.5 * sigma
H = 5 * sigma

cusum_df['C+'] = 0.0
cusum_df['C-'] = 0.0
for i in range(1, len(cusum_df)):
    x = cusum_df.loc[cusum_df.index[i], 'Answer Speed (Seconds)']
    cusum_df.loc[cusum_df.index[i], 'C+'] = max(0, cusum_df.loc[cusum_df.index[i - 1], 'C+'] + (x - target - k))
    cusum_df.loc[cusum_df.index[i], 'C-'] = max(0, cusum_df.loc[cusum_df.index[i - 1], 'C-'] + (target - x - k))
    
m = 10
k = 0.5 * sigma
xc = len(cusum_df)
yc = cusum_df['C+'].iloc[-1]

v_mask_x = [xc - m, xc, xc - m]
v_mask_y = [yc + k * m, yc, yc - k * m]

plt.figure(figsize=(14, 6))
plt.plot(range(1, len(cusum_df) + 1), cusum_df['C+'], color='red', label='C+ (cumulative increase)')
plt.plot(range(1, len(cusum_df) + 1), cusum_df['C-'], color='blue', label='C− (cumulative decrease)')
plt.axhline(H, linestyle='--', color='black', label='Control limit H')
plt.plot(v_mask_x, v_mask_y, linestyle='--', color='black', label='V-mask')
plt.title('CUSUM Chart: Average Answer Time')
plt.xlabel('Day')
plt.ylabel('Cumulative Deviation (sec)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
