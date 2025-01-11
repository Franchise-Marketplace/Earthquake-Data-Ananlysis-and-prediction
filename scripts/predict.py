import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import time

script_dir = os.path.dirname(os.path.abspath(__file__))

# Function for reverse geocoding to get location name based on latitude and longitude
def get_location_name(latitude, longitude, geolocator, retries=3, timeout=10):
    for attempt in range(retries):
        try:
            location = geolocator.reverse((latitude, longitude), language='en', timeout=timeout)
            return location.address if location else "Unknown Location"
        except GeocoderTimedOut:
            print(f"Timeout error, retrying... (Attempt {attempt+1}/{retries})")
            time.sleep(5)  # Wait before retrying
        except Exception as e:
            print(f"Error in reverse geocoding: {e}")
            break
    return "Unknown Location"

def make_prediction():
    # File paths
    model_file = os.path.join(script_dir, "../model/earthquake_model.pkl")
    processed_data_path = os.path.join(script_dir, "../data/processed/new_ethiopian_earthquakes_cleaned_sample.csv") 
    prediction_data_path = os.path.join(script_dir, "../data/prediction")

    # Create the directory if it doesn't exist
    os.makedirs(prediction_data_path, exist_ok=True)

    # Load the model
    model = joblib.load(model_file)
    print(f"Model loaded from: {model_file}")

    # Initialize Geolocator for reverse geocoding
    geolocator = Nominatim(user_agent="earthquake_predictor")

    # Load processed data
    df = pd.read_csv(processed_data_path)

    # Sample new data for prediction
    new_sample_data = df[['latitude', 'longitude', 'depth']].iloc[:100]

    # Predict earthquake magnitudes for the new data
    predictions = model.predict(new_sample_data)

    # Collect prediction results and locations
    prediction_results = []
    for i, (lat, lon, depth, pred) in enumerate(zip(new_sample_data['latitude'], new_sample_data['longitude'], new_sample_data['depth'], predictions)):
        location_name = get_location_name(lat, lon, geolocator)

        # Only add to results if location is not "Unknown Location"
        if location_name != "Unknown Location":
            prediction_results.append({
                'Location': location_name,
                'Latitude': lat,
                'Longitude': lon,
                'Depth': depth,
                'Predicted Magnitude': pred
            })
            print(f'Sample {i+1}: {location_name} magnitude: {pred}   {lat} {lon}')
        else:
            print(f'Sample {i+1}: Location is unknown, skipping...')

    # Create DataFrame with valid data
    prediction_df = pd.DataFrame(prediction_results)

    # If there are any valid predictions, save them
    if not prediction_df.empty:
        prediction_df.to_csv(os.path.join(script_dir, "../data/prediction/earthquake_prediction.csv"))
        print(f"Predictions saved to: {os.path.join(script_dir, '../data/prediction/earthquake_prediction.csv')}")
    else:
        print("No valid predictions to save.")

    # Plot 1: Latitude and Longitude of the most frequent earthquakes
    most_frequent = prediction_df.groupby(['Latitude', 'Longitude']).size().reset_index(name='Frequency')
    top_frequent = most_frequent.nlargest(10, 'Frequency')
    plt.figure(figsize=(10, 6))
    for _, row in top_frequent.iterrows():
        plt.scatter(row['Longitude'], row['Latitude'], label=f"{row['Latitude']}, {row['Longitude']}", s=row['Frequency']*10, alpha=0.7)
    plt.title('Most Frequent Earthquake Locations')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend(title='Lat, Lon', loc='upper left', fontsize='small')
    frequent_plot_path = os.path.join(prediction_data_path, "frequent_locations.png")
    plt.savefig(frequent_plot_path)
    plt.close()
    print(f"Plot 1 saved to: {frequent_plot_path}")

    # Plot 2: Top 5 places (frequency vs magnitude)
    top_places = prediction_df['Location'].value_counts().nlargest(5)
    top_places_df = prediction_df[prediction_df['Location'].isin(top_places.index)]
    plt.figure(figsize=(10, 6))
    for place in top_places.index:
        place_data = top_places_df[top_places_df['Location'] == place]
        plt.scatter([top_places[place]] * len(place_data), place_data['Predicted Magnitude'], label=place, s=50, alpha=0.7)
    plt.title('Top 5 Places by Frequency (Frequency vs Magnitude)')
    plt.xlabel('Frequency')
    plt.ylabel('Predicted Magnitude')
    plt.legend(title='Place', loc='upper right', fontsize='small')
    top_places_plot_path = os.path.join(prediction_data_path, "top_places_frequency_vs_magnitude.png")
    plt.savefig(top_places_plot_path)
    plt.close()
    print(f"Plot 2 saved to: {top_places_plot_path}")
