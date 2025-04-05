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
ewma_df = df.head(60).copy()
ewma_df['Answer Speed (Seconds)'] = pd.to_timedelta(ewma_df['Answer Speed (AVG)']).dt.total_seconds()
ewma_df = ewma_df.dropna(subset=['Answer Speed (Seconds)'])
lambda_ = 0.4
L = 3

mu = ewma_df['Answer Speed (Seconds)'].mean()
sigma = ewma_df['Answer Speed (Seconds)'].std()
ewma_df['EWMA'] = ewma_df['Answer Speed (Seconds)'].ewm(alpha=lambda_, adjust=False).mean()

n = len(ewma_df)
ewma_df['UCL'] = mu + L * sigma * np.sqrt(lambda_ / (2 - lambda_) * (1 - (1 - lambda_) ** (2 * np.arange(1, n + 1))))
ewma_df['LCL'] = mu - L * sigma * np.sqrt(lambda_ / (2 - lambda_) * (1 - (1 - lambda_) ** (2 * np.arange(1, n + 1))))


plt.figure(figsize=(14, 6))
plt.plot(ewma_df.index + 1, ewma_df['EWMA'], color='blue', marker='o', label='EWMA')
plt.plot(ewma_df.index + 1, ewma_df['UCL'], linestyle='--', color='red', label='UCL')
plt.plot(ewma_df.index + 1, ewma_df['LCL'], linestyle='--', color='green', label='LCL')
plt.axhline(mu, color='gray', linestyle='-', label='Mean (μ)')

plt.title('EWMA-карта: Answer Speed (60 days)')
plt.xlabel('Day')
plt.ylabel('Answer Speed (Seconds)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()