import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the library containing the CSV files
library_path = './CSV_data'  # Change this path to your library folder

# List of CSV file names
csv_files = ['T_power_data.csv', 'R_power_data.csv']

# Create a figure with two subplots side by side
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Iterate over the CSV files and plot the power vs frequency
for i, csv_file in enumerate(csv_files):
    csv_path = os.path.join(library_path, csv_file)
    df = pd.read_csv(csv_path)

    # Extract the data for plotting
    frequency = df['Frequency (Hz)']
    power = df['Power (mW)']

    # Plot the data on the respective subplot
    axes[i].plot(frequency, power, label='Power (mW)', color='green')

    # Set labels and title for the subplot
    axes[i].set_xlabel('Frequency (Hz)')
    axes[i].set_ylabel('Power (mW)')
    axes[i].set_title(f'{csv_file.split(".")[0]} - Power vs. Frequency')
    axes[i].legend()

    # Save the plot in the same library as the input CSV files
    output_file = os.path.join(library_path, f'{csv_file.split(".")[0]}_power_plot.png')
    plt.savefig(output_file)

# Adjust spacing between subplots
plt.tight_layout()

# Show the plots
plt.show()
