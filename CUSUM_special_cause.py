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


# === Загрузка и подготовка данных ===
df.columns = df.columns.str.strip()
df = df[['Date', 'Resolved']].dropna().copy()
df['ResolvedBinary'] = df['Resolved'].str.upper().str.strip().apply(lambda x: 1 if x == 'Y' else 0)
df['Date'] = pd.to_datetime(df['Date'])
daily = df.groupby(df['Date'].dt.date).agg(p_i=('ResolvedBinary', 'mean')).reset_index()
daily['Date'] = pd.to_datetime(daily['Date'])

# === Параметры CUSUM и маски ===
mu_0 = daily['p_i'].mean()
sigma = daily['p_i'].std()
k = 0.5 * sigma
h = 5 * k

# === CUSUM ===
daily['CUSUM'] = (daily['p_i'] - mu_0).cumsum()

# === Маска на выбранной дате (например, 17 января) ===
mask_center_date = pd.to_datetime("2016-01-17")
mask_idx = daily[daily['Date'] == mask_center_date].index[0]
mask_center_y = daily.loc[mask_idx, 'CUSUM']

# === Расчёт границ маски ===
steps = 6
forward_indices = list(range(mask_idx, min(mask_idx + steps + 1, len(daily))))
future_dates = daily['Date'].iloc[forward_indices]
cusum_vals = daily['CUSUM'].iloc[forward_indices]

v_upper = mask_center_y - h + k * (np.arange(len(forward_indices)))
v_lower = mask_center_y + h - k * (np.arange(len(forward_indices)))

# === Поиск точек-нарушений ===
violations = daily.iloc[forward_indices].copy()
violations['Upper'] = v_upper
violations['Lower'] = v_lower
violations['Violation'] = (violations['CUSUM'] > violations['Upper']) | (violations['CUSUM'] < violations['Lower'])

# === Построение графика ===
plt.figure(figsize=(14, 6))
plt.plot(daily['Date'], daily['CUSUM'], marker='o', color='tab:blue', label='CUSUM')
plt.axhline(0, color='green', linestyle='--', label='Center Line')

# Границы маски
plt.plot(future_dates, v_upper, '--', color='red', linewidth=2, label='V-mask Upper')
plt.plot(future_dates, v_lower, '--', color='red', linewidth=2, label='V-mask Lower')
plt.scatter(mask_center_date, mask_center_y, color='black', zorder=5, label='V-mask Apex')

# Нарушения
violating_points = violations[violations['Violation']]
plt.scatter(violating_points['Date'], violating_points['CUSUM'], color='crimson', label='Violation', zorder=6)

# Финальные настройки
plt.title('CUSUM Chart with V-mask and Highlighted Violations')
plt.xlabel('Date')
plt.ylabel('CUSUM Value')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
