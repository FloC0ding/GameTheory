import matplotlib.pyplot as plt
import numpy as np

# Sample data
data = [10, 15, 7, 12]
categories = ['A', 'B', 'C', 'D']

# Create x-axis values
x = np.arange(len(data))

# Specify the indices of bars to modify
indices_to_change = [1, 3]  # Adjust the indices as needed

# Specify the new heights for the selected bars
new_heights = [20, 10]  # Adjust the heights as needed

# Modify the data for the selected bars
for index, new_height in zip(indices_to_change, new_heights):
    data[index] = new_height

# Create a bar plot with modified heights
plt.bar(x, data)

# Customize the plot
plt.xlabel('Categories')
plt.ylabel('Values')
plt.title('Bar Graph')

# Set the x-axis tick labels
plt.xticks(x, categories)

# Show the plot
plt.show()
