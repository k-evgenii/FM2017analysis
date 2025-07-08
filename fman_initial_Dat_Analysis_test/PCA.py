import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import os


# Path to your CSV file
csv_file = "/home/kondr/football_manager_proj/fman_initial_Dat_Analysis_test/fbmandataset.csv"
# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Load the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file)


