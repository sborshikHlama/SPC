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

# Оставим нужные столбцы и удалим пропуски
df_ewma = df[['Date', 'AvgTalkDuration']].copy()
df_ewma.dropna(inplace=True)

# Преобразуем datetime.time в секунды вручную
def time_to_seconds(t):
    if pd.isnull(t):
        return None
    return t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1e6

df_ewma['AvgTalkDuration_sec'] = df_ewma['AvgTalkDuration'].apply(time_to_seconds)

# Средняя длительность разговора по дням
avg_talk_by_day = df_ewma.groupby(df_ewma['Date'].dt.date).agg(
    AvgTalkDuration_mean=('AvgTalkDuration_sec', 'mean')
).reset_index()

# EWMA параметры
lambda_ = 0.2
L = 3
mu_0 = avg_talk_by_day['AvgTalkDuration_mean'].mean()
sigma = avg_talk_by_day['AvgTalkDuration_mean'].std()

# Расчёт EWMA и контрольных пределов
ewma_values, ucl_values, lcl_values = [], [], []
ewma_prev = mu_0

for i, row in enumerate(avg_talk_by_day.itertuples(), start=1):
    xi = row.AvgTalkDuration_mean
    ewma = lambda_ * xi + (1 - lambda_) * ewma_prev
    ewma_values.append(ewma)
    ewma_prev = ewma

    std_i = sigma * ((lambda_ / (2 - lambda_)) * (1 - (1 - lambda_)**(2 * i)))**0.5
    ucl = mu_0 + L * std_i
    lcl = mu_0 - L * std_i
    ucl_values.append(ucl)
    lcl_values.append(max(0, lcl))

# Добавим данные в таблицу
avg_talk_by_day['EWMA'] = ewma_values
avg_talk_by_day['UCL'] = ucl_values
avg_talk_by_day['LCL'] = lcl_values
avg_talk_by_day['CL'] = mu_0

# Построим график

plt.figure(figsize=(14, 6))
plt.plot(avg_talk_by_day['Date'], avg_talk_by_day['AvgTalkDuration_mean'], label='Daily Average', linestyle=':', alpha=0.5)
plt.plot(avg_talk_by_day['Date'], avg_talk_by_day['EWMA'], color='blue', marker='o', label='EWMA')
plt.plot(avg_talk_by_day['Date'], avg_talk_by_day['CL'], color='green', linestyle='--', label='CL (Mean)')
plt.plot(avg_talk_by_day['Date'], avg_talk_by_day['UCL'], color='red', linestyle='--', label='UCL')
plt.plot(avg_talk_by_day['Date'], avg_talk_by_day['LCL'], color='red', linestyle='--', label='LCL')
plt.title('EWMA Chart: Average Talk Duration (seconds)')
plt.xlabel('Date')
plt.ylabel('Average Talk Duration (sec)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()