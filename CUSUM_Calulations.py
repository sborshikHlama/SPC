import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import kagglehub
import os

path = kagglehub.dataset_download("drnimishadavis/call-center-performance-data")
files = os.listdir(path)
filename = next(f for f in files if f.endswith(".xlsx"))
ful_path = os.path.join(path, filename)
df = pd.read_excel(ful_path)
result_df = pd.DataFrame()

# Clear Data
df = df[['Call Id', 'Date', 'Resolved']].dropna()
df['Date'] = pd.to_datetime(df['Date'])

# Remove hours from Date
df['DateOnly'] = df['Date'].dt.date
df['Resolved'] = df['Resolved'].str.upper().str.strip()
df['Resolved'] = df['Resolved'].apply(lambda x: 1 if x == 'Y' else 0)

# Count Calls per Day
result_df = df.groupby('DateOnly').agg(Call_Count=('Call Id', 'count'), Resolved=('Resolved', 'sum')).reset_index()
result_df['p_i'] = result_df['Resolved'] / result_df['Call_Count']
mu_0_value = result_df['p_i'].mean() 
result_df['mu_0'] = mu_0_value
result_df['CUSUM'] = (result_df['p_i'] - result_df['mu_0']).cumsum()

# CUSUM: C+ and C-

K = 0.5 * result_df['p_i'].std()  # Sensativity
H = 5 * K  # Control Limit

result_df['C_plus'] = 0.0
result_df['C_minus'] = 0.0

for i in range(1, len(result_df)):
    x = result_df.loc[i, 'p_i']
    c_plus_prev = result_df.loc[i - 1, 'C_plus']
    c_minus_prev = result_df.loc[i - 1, 'C_minus']

    result_df.loc[i, 'C_plus'] = max(0, c_plus_prev + (x - mu_0_value - K))
    result_df.loc[i, 'C_minus'] = max(0, c_minus_prev + (mu_0_value - x + K))

result_df['OutOfControl'] = (result_df['C_plus'] > H) | (result_df['C_minus'] > H)

print(result_df)
result_df.to_excel("Cusum_calculations.xlsx", index=False)


# Build Graph
plt.figure(figsize=(14, 6))
plt.plot(result_df['DateOnly'], result_df['CUSUM'], marker='o', color='blue', label='CUSUM')
plt.axhline(0, color='green', linestyle='--', label='Center Line (CUSUM = 0)')
plt.xticks(rotation=45)
plt.title('CUSUM Chart for Resolved Calls (pᵢ)')
plt.xlabel('Date')
plt.ylabel('CUSUM Value')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Cusum Shifts
plt.figure(figsize=(14, 6))
plt.plot(result_df['DateOnly'], result_df['C_plus'], label='C⁺ (positive shifts)', color='blue', marker='o')
plt.plot(result_df['DateOnly'], result_df['C_minus'], label='C⁻ (negative shifts)', color='red', marker='o')
plt.axhline(H, color='gray', linestyle='--', label=f'Control Limit (H = {H:.4f})')
plt.xticks(rotation=45)
plt.title('One-sided CUSUM Chart (C⁺ and C⁻) for Resolved Calls')
plt.xlabel('Date')
plt.ylabel('CUSUM Value')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
