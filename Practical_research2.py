import matplotlib.pyplot as plt
import numpy as np

# Individual observations (Speed of Answer)
individuals = [109, 70, 10, 53, 95, 24, 22, 15, 78, 50, 84, 89, 48, 63, 45, 101, 74, 89, 68, 97,
               39, 51, 106, 107, 22, 122, 57, 53, 119, 20, 52, 74, 49, 27, 100, 45, 98, 25, 107, 104,
               13, 119, 35, 83, 48, 45, 65, 50, 17, 96, 90, 98, 90, 98, 70, 69, 120, 113, 10, 122,
               125, 33, 51, 58, 121, 118, 52, 55, 68, 106, 32, 45, 119, 46, 101, 56, 80, 24, 113, 19,
               45, 95, 79, 22, 38, 112, 65, 55, 19, 53, 24, 73, 55, 23, 124, 103, 69, 78, 78, 44]

# Moving ranges
moving_ranges = [39, 60, 43, 42, 71, 2, 7, 63, 28, 34, 5, 41, 15, 18, 56, 27, 15, 21, 29, 58,
                 12, 55, 1, 85, 100, 65, 4, 66, 99, 32, 22, 25, 22, 73, 55, 53, 73, 82, 3, 91,
                 106, 84, 48, 35, 3, 20, 15, 33, 79, 6, 8, 8, 8, 28, 1, 51, 7, 103, 112, 3,
                 92, 18, 7, 63, 3, 66, 3, 13, 38, 74, 13, 74, 73, 55, 45, 24, 56, 89, 94, 26,
                 50, 16, 57, 16, 74, 47, 10, 36, 34, 29, 49, 18, 32, 101, 21, 34, 9, 0, 34]

# Observation numbers (1 to 100 for I chart, 2 to 100 for MR chart)
obs_numbers_i = np.arange(1, 101)
obs_numbers_mr = np.arange(2, 101)

# Control limits and centerlines
x_bar = 67.97
ucl_i = 181.625
lcl_i = 0  # Adjusted to 0 since Speed of Answer cannot be negative

mr_bar = 42.727
ucl_mr = 139.589
lcl_mr = 0

# Plot the Individual (I) Chart
plt.figure(figsize=(12, 6))
plt.plot(obs_numbers_i, individuals, marker='o', label='Individual Speed of Answer', color='blue')
plt.axhline(y=x_bar, color='green', linestyle='--', label=f'Center Line (X-bar = {x_bar:.2f})')
plt.axhline(y=ucl_i, color='red', linestyle='--', label=f'UCL = {ucl_i:.2f}')
plt.axhline(y=lcl_i, color='red', linestyle='--', label=f'LCL = {lcl_i}')
plt.title('Individual (I) Chart for Speed of Answer (First 100 Answered Calls)')
plt.xlabel('Observation Number')
plt.ylabel('Speed of Answer (seconds)')
plt.legend()
plt.grid(True)
plt.xticks(np.arange(1, 101, step=5))
plt.savefig('individual_chart.png')
plt.show()

# Plot the Moving Range (MR) Chart
plt.figure(figsize=(12, 6))
plt.plot(obs_numbers_mr, moving_ranges, marker='o', label='Moving Range', color='blue')
plt.axhline(y=mr_bar, color='green', linestyle='--', label=f'Center Line (MR-bar = {mr_bar:.2f})')
plt.axhline(y=ucl_mr, color='red', linestyle='--', label=f'UCL = {ucl_mr:.2f}')
plt.axhline(y=lcl_mr, color='red', linestyle='--', label=f'LCL = {lcl_mr}')
plt.title('Moving Range (MR) Chart for Speed of Answer (First 100 Answered Calls)')
plt.xlabel('Observation Number')
plt.ylabel('Moving Range (seconds)')
plt.legend()
plt.grid(True)
plt.xticks(np.arange(2, 101, step=5))
plt.savefig('moving_range_chart.png')
plt.show()