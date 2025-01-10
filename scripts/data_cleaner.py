import pandas as pd
import numpy as np

# Assuming your data is in a DataFrame called `df`
# Replace `data` with your loaded data dictionary
data = "../data/raw/ethiopian_earthquakes.csv"

df = pd.read_csv(data)

df = pd.DataFrame(df)

# Convert 'time' column to datetime
df['time'] = pd.to_datetime(df['time'], unit='ms')

# Handle missing values
df = df.dropna()

# Remove duplicates
df = df.drop_duplicates()

# Define thresholds for noise removal
magnitude_threshold = 3  # Remove earthquakes with invalid or zero magnitude
depth_threshold = 700    # Remove earthquakes with depth greater than 700 km (too deep)

# Remove noisy data
df = df[(df['magnitude'] > magnitude_threshold) & (df['depth'] <= depth_threshold)]


# Sort by time to calculate time differences
df = df.sort_values(by='time')

# Add a feature for time since the last earthquake (in days)
df['time_since_last_quake'] = df['time'].diff().dt.total_seconds() / (60 * 60 * 24)
df['time_since_last_quake'].fillna(0, inplace=True)

# Add a feature for large magnitudes
df['is_large_magnitude'] = (df['magnitude'] >= 5.0).astype(int)

# Label depth into categories
def label_depth(depth):
    if depth <= 70:
        return 'Shallow'
    elif 70 < depth <= 300:
        return 'Intermediate'
    else:
        return 'Deep'

df['depth_label'] = df['depth'].apply(label_depth)

# Display cleaned data
print(df.info())
print(df.head())

df.to_csv("../data/processed/ethiopian_earthquakes_cleaned.csv")


