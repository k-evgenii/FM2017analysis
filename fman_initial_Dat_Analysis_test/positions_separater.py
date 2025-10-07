import pandas as pd
import os

# Path to your CSV file
csv_file = r"D:\Projects\Github projects\FM2017analysis\fman_initial_Dat_Analysis_test\fbmandataset.csv"
# Load the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file)

# Extract the 74th column (PositionsDesc) into a separate array
positions_desc = df.iloc[:, 73]  # 74th column (0-based index is 73)

# Initialize a set to store unique positions
unique_positions = set()

# Process each cell in the PositionsDesc column
for cell in positions_desc.dropna():  # Drop NaN values
    # Ensure the cell is a string
    cell = str(cell)
    # Split positions by '/', then split combined positions into individual ones
    for position_combination in cell.split("/"):
        individual_positions = position_combination.split()  # Split combined positions (e.g., "DM RL")
        unique_positions.update(individual_positions)  # Add individual positions to the set

# Create a dictionary of unique positions with sequential numbers
pos_map1 = {position: index + 1 for index, position in enumerate(sorted(unique_positions))}

# Print the resulting pos_map
print("Position Map:", pos_map1)