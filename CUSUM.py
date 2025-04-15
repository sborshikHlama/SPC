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

df_cusum = df[['Date', 'Resolved']].dropna().copy()
df_cusum['ResolvedBinary'] = df_cusum['Resolved'].str.upper().str.strip().apply(lambda x: 1 if x == 'Y' else 0)
resolved_by_day = df_cusum.groupby(df_cusum['Date'].dt.date).agg(
    p_i=('ResolvedBinary', 'mean')
).reset_index()

# Расчёт CUSUM
mu_0 = resolved_by_day['p_i'].mean()
resolved_by_day['CUSUM'] = (resolved_by_day['p_i'] - mu_0).cumsum()
n = len(resolved_by_day)
k = 0.5 * resolved_by_day['p_i'].std()
h = 5 * k

# Определим позиции для масок — равномерно от последней точки назад
mask_indices = list(range(n - 1, -1, -7))[:4]  # каждые 7 шагов от конца, максимум 4 маски

# Построение графика
plt.figure(figsize=(14, 6))
plt.plot(resolved_by_day['Date'], resolved_by_day['CUSUM'], marker='o', label='CUSUM', color='tab:blue')
plt.axhline(0, color='green', linestyle='--', linewidth=1)

# Наложение V-масок
for idx in mask_indices:
    center_date = resolved_by_day['Date'].iloc[idx]
    center_y = resolved_by_day['CUSUM'].iloc[idx]

    # Построение вперёд (5 дней)
    forward_x = np.arange(1, 6)
    future_dates = pd.date_range(start=center_date, periods=6, freq='D')[1:]

    mask_upper_dates = pd.concat([pd.Series([center_date]), pd.Series(future_dates)])
    mask_upper_values = pd.Series([center_y - h] + list(center_y - h + k * forward_x))

    mask_lower_dates = pd.concat([pd.Series([center_date]), pd.Series(future_dates)])
    mask_lower_values = pd.Series([center_y + h] + list(center_y + h - k * forward_x))

    # Отрисовка маски
    plt.plot(mask_upper_dates, mask_upper_values, linestyle='--', color='red', alpha=0.6)
    plt.plot(mask_lower_dates, mask_lower_values, linestyle='--', color='red', alpha=0.6)


plt.title('CUSUM Chart with Multiple Forward V-masks')
plt.xlabel('Date')
plt.ylabel('CUSUM Value')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(['CUSUM', 'Center Line (0)', 'V-mask boundaries'], loc='upper left')
plt.tight_layout()
plt.show()