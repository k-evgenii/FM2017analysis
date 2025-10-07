import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from dateutil.relativedelta import relativedelta
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

# ————————————————
# 1. Load & preprocess exactly as you had it
# ————————————————
csv_file  = r"D:\Projects\Github projects\FM2017analysis\fman_initial_Dat_Analysis_test\fbmandataset.csv"
df        = pd.read_csv(csv_file)

# drop text columns
if 'Name' in df: df = df.drop(columns=['Name'])
if 'Born' in df: df = df.drop(columns=['Born'])
if 'PositionsDesc' in df:
    df['PositionsDesc'] = df['PositionsDesc'].astype(str)

# map positions → lists of ints
pos_map = {
  "GK":1,"RB":2,"LB":3,"CB":4,"DM":6,"RM":7,"RW":7,"CM":8,
  "ST":9,"CF":9,"AM":10,"SS":10,"LM":11,"LW":11,"WB":5,
  "RL":2,"RF":9,"LF":9,"D":4,"C":8,"LC":4,"RC":4,"RLC":4,
  "M":8,"S":9,"R":9
}
def map_positions_to_numbers(position_str):
    parts = [p.strip() 
             for seg in str(position_str).split("/") 
             for p in seg.split() 
             if p.strip()]
    return [pos_map[p] for p in parts if p in pos_map]

df['PositionNumbers'] = df['PositionsDesc']\
                           .apply(lambda x: map_positions_to_numbers(x))

df = df.drop(columns=['PositionsDesc'])

# ————————————————
# 2. Turn your PositionNumbers into real numeric columns
# ————————————————
mlb    = MultiLabelBinarizer()
pos_mat= mlb.fit_transform(df['PositionNumbers'])
pos_df = pd.DataFrame(
    pos_mat,
    columns=[f"Pos_{c}" for c in mlb.classes_],
    index=df.index
)
df = pd.concat([df, pos_df], axis=1).drop(columns=['PositionNumbers'])

# ————————————————
# 3. Build your numeric matrix & standardize
# ————————————————
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
X            = df[numeric_cols].values.astype(np.float32)

scaler       = StandardScaler()
X_scaled     = scaler.fit_transform(X)

# ————————————————
# 4. PCA with 2 components
# ————————————————
pca2         = PCA(n_components=2)
X_pca2       = pca2.fit_transform(X_scaled)   # shape (n_samples,2)

# attach PC1 & PC2 back to your original df
df['PC1']    = X_pca2[:,0]
df['PC2']    = X_pca2[:,1]

print("Explained variance (PC1,PC2):", pca2.explained_variance_ratio_)
print(df[['PC1','PC2']].head())

# ————————————————
# 5. (Optional) Reconstruct original data from just PC1&PC2
# ————————————————
# 5a) map the 2D scores back into scaled-space
X_approx_scaled = pca2.inverse_transform(X_pca2)

# 5b) undo the StandardScaler
X_approx = scaler.inverse_transform(X_approx_scaled)

# 5c) DataFrame of your rank-2 reconstruction
recon_df = pd.DataFrame(
    X_approx,
    columns=numeric_cols,
    index=df.index
)
print("Reconstructed (first rows):")
print(recon_df.head())

# ————————————————
# 6. (Optional) Visualize PC1 vs PC2
# ————————————————
plt.figure(figsize=(8,6))
plt.scatter(df['PC1'], df['PC2'], s=8, alpha=0.4)
plt.xlabel("PC1"); plt.ylabel("PC2")
plt.title("PCA (2 components)")
plt.grid(True)
plt.show()
