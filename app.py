from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from geopy.geocoders import Nominatim
import math

# Importing the data processing functions from the 'scripts' folder
from scripts.data_cleaner import clean_data
from scripts.data_cleaner_sample import sample_clean_data
from scripts.data_fetch_api import fetch_data
from scripts.model_train import train_model
from scripts.predict import make_prediction
from scripts.data_exploration import explore_data

app = Flask(__name__)

# Directory for storing data and images in the root folder
root_dir = os.path.dirname(__file__)

# Directory for storing images (this is the location where your images are)
image_dir = os.path.join(root_dir, 'data/prediction')
os.makedirs(image_dir, exist_ok=True)

# Directory for storing data
data_dir = os.path.join(root_dir, 'data')
prediction_data_path = os.path.join(data_dir, 'prediction', 'earthquake_prediction.csv')

# Route for homepage
@app.route('/')
def index():
    # Read the prediction data
    prediction_data = pd.read_csv(prediction_data_path)



    # Pagination variables
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = math.ceil(len(prediction_data) / per_page)

    # Get the subset of data for this page
    data_subset = prediction_data.iloc[start:end]

    # Return the HTML page with data
    return render_template('index.html', 
                           plot_img_1=url_for('serve_images', filename='frequent_locations.png'),  # Correct file path
                           plot_img_2=url_for('serve_images', filename='top_places_frequency_vs_magnitude.png'),  # Correct file path
                           data=data_subset, page=page, total_pages=total_pages)

# Route to download the CSV file
@app.route('/download_csv')
def download_csv():
    return send_from_directory(data_dir, 'prediction/earthquake_prediction.csv')

# Custom route to serve images from 'data/prediction' folder
@app.route('/data/prediction/<filename>')
def serve_images(filename):
    return send_from_directory(image_dir, filename)

# Route to update data and trigger the cleaning and prediction functions
@app.route('/update_data', methods=['POST'])
def update_data():
    # Running the data processing functions
    fetch_data()
    clean_data()
    sample_clean_data()
    explore_data()
    train_model()
    make_prediction()

    # Redirect back to the homepage after update
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
