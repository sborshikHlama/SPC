import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import kagglehub
import os

path = kagglehub.dataset_download("satvicoder/call-center-data")

files = os.listdir(path)


filename = next(f for f in files if f.endswith(".csv"))
ful_path = os.path.join(path, filename)
df = pd.read_csv(ful_path)
sample_df = df.head(60).copy()

sample_df['Answer Speed (Seconds)'] = pd.to_timedelta(sample_df['Answer Speed (AVG)']).dt.total_seconds()
sample_df = sample_df.dropna(subset=['Answer Speed (Seconds)'])

x_values = sample_df['Answer Speed (Seconds)'].values
moving_ranges = np.abs(np.diff(x_values))

x_bar = np.mean(x_values)
mr_bar = np.mean(moving_ranges)

UCL_X = x_bar + 2.66 * mr_bar
LCL_X = x_bar - 2.66 * mr_bar

UCL_mR = 3.267 * mr_bar

plt.figure(figsize=(14, 6))
plt.plot(range(1, len(x_values) + 1), x_values, marker='o', color='blue', label='Answer Speed (seconds)')
plt.axhline(x_bar, color='gray', linestyle='-', label='Mean (X̄)')
plt.axhline(UCL_X, linestyle='--', color='red', label='UCL')
plt.axhline(LCL_X, linestyle='--', color='green', label='LCL')
plt.title('X-chart: Answer speed (seconds)')
plt.xlabel('Day')
plt.ylabel('Answer speed (seconds)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 4))
plt.plot(range(2, len(x_values) + 1), moving_ranges, marker='o', color='purple', label='Moving Range')
plt.axhline(mr_bar, color='gray', linestyle='-', label='Mean mR')
plt.axhline(UCL_mR, linestyle='--', color='red', label='UCL (mR)')
plt.title('mR-chart: Moving Range (Response Time)')
plt.xlabel('Day')
plt.ylabel('|Δ of time| (seconds)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
