## We wanted to perform an explanatory analysis of player attributes in Football Manager 2017. We have selected
## key attributes to analyse their distributions and correlations.

import sqlite3
import pandas as pd
# Replace with the full path to your FM17 database file
db_file = r"C:\Users\Niall\OneDrive\Documents\University\Year 4\fm project\FM2017analysis\db-setup\fm.db"
conn = sqlite3.connect(db_file)

  
import sqlite3
import pandas as pd

# Path to the SQLite database
db_file = r"C:\Users\Niall\OneDrive\Documents\University\Year 4\fm project\FM2017analysis\db-setup\fm.db"

conn = sqlite3.connect(db_file)
query = """
SELECT
    name,
    age,
    acceleration,
    pace,
    passing,
    finishing,
    tackling,
    vision,
    strength,
    stamina,
    technique,
    dribbling
FROM Players
"""
df = pd.read_sql_query(query, conn)
conn.close()
import matplotlib.pyplot as plt
import seaborn as sns

attributes = [
    "acceleration", "pace", "passing", "finishing", "tackling",
    "vision", "strength", "stamina", "technique", "dribbling"
]

# Histograms
df[attributes].hist(bins=20, figsize=(14, 10), edgecolor="black")
plt.suptitle("Distribution of Player Attributes (All Players)", fontsize=16)
plt.tight_layout()
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df[attributes].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Attribute Correlation Heatmap (All Players)", fontsize=14)
plt.show()
