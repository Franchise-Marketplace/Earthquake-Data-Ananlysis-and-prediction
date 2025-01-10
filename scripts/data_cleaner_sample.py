import pandas as pd
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

def sample_clean_data():
    # Load new sample data 

    data = os.path.join(script_dir, "../data/raw/ethiopian_earthquakes.csv"  )

    df = pd.read_csv(data)

    # Convert 'time' column to datetime (if applicable)
    df['time'] = pd.to_datetime(df['time'], unit='ms')

    # Handle missing values (drop rows with missing values)
    df = df.dropna()

    # Remove duplicates
    df = df.drop_duplicates()

    # Define thresholds for noise removal
    magnitude_threshold = 3  # Remove earthquakes with invalid or zero magnitude
    depth_threshold = 700    # Remove earthquakes with depth greater than 700 km (too deep)

    # Remove noisy data based on magnitude and depth thresholds
    df = df[(df['magnitude'] > magnitude_threshold) & (df['depth'] <= depth_threshold)]

    # Sort by time in descending order to get the latest earthquakes at the top
    df = df.sort_values(by='time', ascending=False)

    # Add a feature for time since the last earthquake (in days)
    df['time_since_last_quake'] = df['time'].diff().dt.total_seconds() / (60 * 60 * 24)
    df['time_since_last_quake'].fillna(0, inplace=True)

    # Add a feature for large magnitudes (1 if magnitude >= 5, otherwise 0)
    df['is_large_magnitude'] = (df['magnitude'] >= 5.0).astype(int)

    # Label depth into categories (Shallow, Intermediate, Deep)
    def label_depth(depth):
        if depth <= 70:
            return 'Shallow'
        elif 70 < depth <= 300:
            return 'Intermediate'
        else:
            return 'Deep'

    df['depth_label'] = df['depth'].apply(label_depth)

    # Display cleaned data info and first few rows
    print(df.info())
    print("First 5 rows of the cleaned and sorted data:")
    print(df.head())

    # Save the cleaned data to a new CSV file
    df.to_csv(os.path.join(script_dir, "../data/processed/new_ethiopian_earthquakes_cleaned_sample.csv"), index=False)

    # Optionally, you can select the first 5 rows (newest data) for predictions or further analysis
    newest_data = df.head(5)
    print("Newest 5 rows of cleaned data for prediction:")
    print(newest_data)
