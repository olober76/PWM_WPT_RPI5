import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the library containing the CSV files
library_path = './CSV_data'  # Change this path to your library folder

# List of CSV file names
csv_files = ['T_power_data.csv', 'R_power_data.csv']

# Create a figure with two subplots side by side
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Iterate over the CSV files and plot the data
for i, csv_file in enumerate(csv_files):
    csv_path = os.path.join(library_path, csv_file)
    df = pd.read_csv(csv_path)

    # Group the data by 'Frequency (Hz)' and calculate the mean of 'Voltage (V)' and 'Current (mA)'
    grouped = df.groupby('Frequency (Hz)').agg({'Voltage (V)': 'mean', 'Current (mA)': 'mean'}).reset_index()

    # Extract the data for plotting
    frequency = grouped['Frequency (Hz)']
    voltage = grouped['Voltage (V)']
    current = grouped['Current (mA)']

    # Plot the data on the respective subplot
    axes[i].plot(frequency, voltage, label='Voltage (V)')
    axes[i].plot(frequency, current, label='Current (mA)')

    # Set labels and title for the subplot
    axes[i].set_xlabel('Frequency (Hz)')
    axes[i].set_ylabel('Voltage (V) / Current (mA)')
    axes[i].set_title(f'{csv_file} - Voltage and Current vs. Frequency')
    axes[i].legend()

    # Save the plot in the same library as the input CSV files
    output_file = os.path.join(library_path, f'{csv_file.split(".")[0]}_plot.png')
    plt.savefig(output_file)

# Adjust spacing between subplots
plt.tight_layout()

# Show the plots
plt.show()
