import matplotlib.pyplot as plt
import numpy as np

# Data from calculations
subgroups = np.arange(1, 21)  # Subgroup numbers 1 to 20

# Average Chart Data
averages = [67.4, 37.8, 65.8, 85.8, 65, 74.2, 60.4, 75.8, 59.6, 54.6, 89.2, 86.8, 77.6, 79.8, 68.6, 58.4, 55.8, 60.8, 59.8, 74.4]
x_double_bar = 67.97  # Center Line for Average Chart
ucl_x = 113.2645  # Upper Control Limit for Average Chart
lcl_x = 22.6755  # Lower Control Limit for Average Chart

# Range Chart Data
ranges = [99, 63, 44, 33, 85, 102, 73, 82, 106, 79, 28, 112, 92, 66, 87, 94, 73, 93, 101, 59]
r_bar = 78.5  # Center Line for Range Chart
ucl_r = 165.949  # Upper Control Limit for Range Chart
lcl_r = 0  # Lower Control Limit for Range Chart

# Plot the Average (X-bar) Chart
plt.figure(figsize=(12, 6))
plt.plot(subgroups, averages, marker='o', label='Subgroup Averages', color='blue')
plt.axhline(y=x_double_bar, color='green', linestyle='--', label=f'Center Line (X-double-bar = {x_double_bar:.2f})')
plt.axhline(y=ucl_x, color='red', linestyle='--', label=f'UCL = {ucl_x:.2f}')
plt.axhline(y=lcl_x, color='red', linestyle='--', label=f'LCL = {lcl_x:.2f}')
plt.title('Average (X-bar) Chart for Speed of Answer (First 100 Values in Order)')
plt.xlabel('Subgroup')
plt.ylabel('Average Speed of Answer (seconds)')
plt.legend()
plt.grid(True)
plt.xticks(subgroups)
plt.savefig('average_chart_corrected.png')
plt.show()

# Plot the Range (R) Chart
plt.figure(figsize=(12, 6))
plt.plot(subgroups, ranges, marker='o', label='Subgroup Ranges', color='blue')
plt.axhline(y=r_bar, color='green', linestyle='--', label=f'Center Line (R-bar = {r_bar:.2f})')
plt.axhline(y=ucl_r, color='red', linestyle='--', label=f'UCL = {ucl_r:.2f}')
plt.title('Range (R) Chart for Speed of Answer (First 100 Values in Order)')
plt.xlabel('Subgroup')
plt.ylabel('Range of Speed of Answer (seconds)')
plt.legend()
plt.grid(True)
plt.xticks(subgroups)
plt.savefig('range_chart_corrected.png')
plt.show()