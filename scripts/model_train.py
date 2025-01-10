import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib


script_dir = os.path.dirname(os.path.abspath(__file__))

def train_model():
    # File paths
    processed_data_path = os.path.join(script_dir, "../data/processed/ethiopian_earthquakes_cleaned.csv")
    model_path = os.path.join(script_dir, "../model")
    os.makedirs(model_path, exist_ok=True)

    # Load processed data
    df = pd.read_csv(processed_data_path)

    # Features and target
    X = df[['latitude', 'longitude', 'depth']]
    y = df['magnitude']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Absolute Error: {mae}")
    print(f"R2 Score: {r2}")

    # Save the model
    model_file = os.path.join(model_path, "earthquake_model.pkl")
    joblib.dump(model, model_file)
    print(f"Trained model saved to: {model_file}")
