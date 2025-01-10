import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# File paths
data = "../data/processed/ethiopian_earthquakes_cleaned.csv"
output_dir = "../data/processed/plots"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load data
df = pd.read_csv(data)
df = pd.DataFrame(df)

# Ensure the 'time' column is in datetime format
df['time'] = pd.to_datetime(df['time'])

# Plot 1: Distribution of earthquake magnitudes
plt.figure(figsize=(10, 6))
sns.histplot(df['magnitude'], bins=30, kde=True)
plt.title('Magnitude Distribution')
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'magnitude_distribution.png'))
plt.close()

# Plot 2: Earthquake occurrences over time
plt.figure(figsize=(15, 6))
plt.plot(df['time'], df['magnitude'], marker='o', linestyle='-', alpha=0.6)
plt.title('Earthquake Magnitudes Over Time')
plt.xlabel('Time')
plt.ylabel('Magnitude')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'earthquake_magnitudes_over_time.png'))
plt.close()

# Plot 3: Earthquake frequency by place
plt.figure(figsize=(12, 8))
top_places = df['place'].value_counts().nlargest(10)  # Top 10 places with most earthquakes
sns.barplot(y=top_places.index, x=top_places.values, palette='viridis')
plt.title('Top 10 Places with Most Earthquakes')
plt.xlabel('Frequency')
plt.ylabel('Place')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'earthquake_frequency_by_place.png'))
plt.close()

# Plot 4: Depth distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['depth'], bins=30, kde=True, color='purple')
plt.title('Depth Distribution')
plt.xlabel('Depth (km)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'depth_distribution.png'))
plt.close()

print(f"Plots saved in: {output_dir}")
