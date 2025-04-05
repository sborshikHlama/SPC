import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import kagglehub

# Download latest version
path = kagglehub.dataset_download("drnimishadavis/call-center-performance-data")
files = os.listdir(path)
filename = next(f for f in files if f.endswith(".xlsx"))
ful_path = os.path.join(path, filename)
df_calls = pd.read_excel(ful_path)

# Убедимся, что нужные колонки есть и нет пропусков
df_calls = df_calls.dropna(subset=["Speed of Answer", "Date"])

# Создаем колонку только с датой (без времени)
df_calls["DateOnly"] = pd.to_datetime(df_calls["Date"]).dt.date

# Группируем по дате и разбиваем на подгруппы по 5 звонков
grouped = df_calls.groupby("DateOnly")
subgroups = []

for _, group in grouped:
    group = group.sort_values("Date")
    for i in range(0, len(group), 5):
        sub = group.iloc[i:i+5]
        if len(sub) == 5:
            subgroups.append(sub["Speed of Answer"].values)

# Создаем DataFrame, где каждая строка — подгруппа
subgroup_df = pd.DataFrame(subgroups)

# Вычисляем среднее и размах в каждой подгруппе
xbar = subgroup_df.mean(axis=1)
rbar = subgroup_df.max(axis=1) - subgroup_df.min(axis=1)

# Средние значения по всем подгруппам
xbar_bar = xbar.mean()
rbar_bar = rbar.mean()

# Размер подгруппы
n = subgroup_df.shape[1]

# Коэффициенты из таблиц для X̄–R карт (для n = 5)
A2 = 0.577
D3 = 0
D4 = 2.114

# Control limits
UCL_xbar = xbar_bar + A2 * rbar_bar
LCL_xbar = xbar_bar - A2 * rbar_bar
UCL_r = D4 * rbar_bar
LCL_r = D3 * rbar_bar

plt.figure(figsize=(14, 5))
plt.plot(xbar, marker='o', label='X̄ (average speed)')
plt.axhline(xbar_bar, color='black', label='Mean X̄')
plt.axhline(UCL_xbar, color='red', linestyle='--', label='UCL')
plt.axhline(LCL_xbar, color='green', linestyle='--', label='LCL')
plt.title('X̄-chart: Speed of Answer (in subgroups of 5 calls)')
plt.xlabel('Subgroup number')
plt.ylabel('Answer speed (sec)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 5))
plt.plot(rbar, marker='s', color='orange', label='R (размах)')
plt.axhline(rbar_bar, color='black', label='Mean Range')
plt.axhline(UCL_r, color='red', linestyle='--', label='UCL')
plt.axhline(LCL_r, color='green', linestyle='--', label='LCL')
plt.title('R-chart: Answer Speed Range (in subgroups of 5 calls)')
plt.xlabel('Subgroup number')
plt.ylabel('Range (sec)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
