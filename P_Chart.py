import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import kagglehub

# Download the dataset from Kaggle using kagglehub
path = kagglehub.dataset_download("drnimishadavis/call-center-performance-data")

# List all files in the downloaded dataset directory
files = os.listdir(path)

# Find the Excel file in the directory
filename = next(f for f in files if f.endswith(".xlsx"))
ful_path = os.path.join(path, filename)

# Read the Excel file into a DataFrame
df = pd.read_excel(ful_path)

# Clean the "Answered (Y/N)" column by removing whitespace and capitalizing letters
df['Answered (Y/N)'] = df['Answered (Y/N)'].str.upper().str.strip()

# Convert "Y/N" values to binary format: 1 for "Y", 0 for "N"
df['AnsweredBinary'] = df['Answered (Y/N)'].apply(lambda x: 1 if x == 'Y' else 0)

# Group data by date and calculate total calls and number of answered calls
p_chart_data = df.groupby(df['Date'].dt.date).agg(
    total_calls=('AnsweredBinary', 'count'),
    answered_calls=('AnsweredBinary', 'sum')
).reset_index()

# Calculate the proportion of answered calls per day
p_chart_data['p'] = p_chart_data['answered_calls'] / p_chart_data['total_calls']

# Calculate the overall average proportion (center line)
p_bar = p_chart_data['p'].mean()

# Calculate control limits (Upper and Lower Control Limits)
p_chart_data['UCL'] = p_bar + 3 * np.sqrt((p_bar * (1 - p_bar)) / p_chart_data['total_calls'])
p_chart_data['LCL'] = p_bar - 3 * np.sqrt((p_bar * (1 - p_bar)) / p_chart_data['total_calls'])
p_chart_data['CL'] = p_bar  # Center line

# Ensure that the lower control limit is not negative
p_chart_data['LCL'] = p_chart_data['LCL'].apply(lambda x: max(0, x))

# Plot the P-chart
plt.figure(figsize=(14, 6))
plt.plot(p_chart_data['Date'], p_chart_data['p'], color="blue", marker='o', label='Proportion of Answered Calls')
plt.plot(p_chart_data['Date'], p_chart_data['CL'], color='green', linestyle='--', label='CL (Center Line)')
plt.plot(p_chart_data['Date'], p_chart_data['UCL'], color='red', linestyle='--', label='UCL')
plt.plot(p_chart_data['Date'], p_chart_data['LCL'], color='red', linestyle='--', label='LCL')
plt.xticks(rotation=45)
plt.title('P-Chart: Proportion of Answered Calls by Day')
plt.xlabel('Date')
plt.ylabel('Proportion (Answered = Y)')
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()
