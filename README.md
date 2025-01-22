# Earthquake Data Analysis and Prediction

## Introduction

This project involves collecting earthquake data through web scraping or APIs, processing it, and using machine learning techniques for predictive analysis. It also includes data exploration and visualization for better insights.

## Features

- Automated data collection from external sources (e.g., APIs, web scraping).
- Data cleaning and processing to ensure high-quality input for analysis.
- Exploratory Data Analysis (EDA) and visualization.
- Machine learning for earthquake prediction.
- Web-based interface for visualization and interaction.

## Project Structure

```plaintext
project-root/
|
|
├── data/                       # Data storage
│   ├── raw/                    # Raw collected data
│   ├── processed/              # Cleaned and transformed data
│   └── prediction/             # Prediction outputs
|
├── env/                        # Virtual environment (excluded in .gitignore)
|
|
├── model/                      # Trained ML models
│   └── earthquake_model.pkl    # Saved model file
|
├── scripts/                    # Core Python scripts for project workflows
│   ├── __init__.py             # Makes it a Python module
│   ├── __main__.py             # Main entry point (if applicable)
│   ├── data_cleaner_sample.py  # Example of cleaning script
│   ├── data_cleaner.py         # Data cleaning logic
│   ├── data_exploration.py     # Exploratory Data Analysis
│   ├── data_fetch_api.py       # API data fetching
│   ├── model_train.py          # Model training pipeline
│   ├── predict.py              # Prediction script
│   └── scraper.py              # Web scraping logic
|
├── static/images/              # Static assets (e.g., images for the web interface)
|
├── templates/                  # HTML templates for the web interface
│   └── index.html              # Main HTML template
|
├── tests/                      # Unit tests for scripts
|
├── app.py                      # Entry point for the web application
├── ethiopian_earthquakes.csv   # Sample dataset for Ethiopia earthquakes
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── .gitignore                  # Files and directories to ignore in version control
```

## Installation and Setup

### Prerequisites

- Python 3.7+
- Virtual environment (optional but recommended)

### Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Franchise-Marketplace/Earthquake-Data-Ananlysis-and-prediction.git
   cd earthquake-analysis
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv env
   source env/bin/activate   # On Windows: .\env\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Data Collection

- **Fetch data from APIs**:
  ```bash
  python scripts/data_fetch_api.py
  ```
- **Scrape data**:
  ```bash
  python scripts/scraper.py
  ```

### Data Cleaning

- Run the data cleaning script:
  ```bash
  python scripts/data_cleaner.py
  ```

### Exploratory Data Analysis

- Use the `data_exploration.py` script or explore the data in Jupyter notebooks located in the `notebooks/` directory.

### Train Machine Learning Model

- Train the model with:
  ```bash
  python scripts/model_train.py
  ```

### Make Predictions

- Run the prediction script:
  ```bash
  python scripts/predict.py
  ```

### Web Application

- Start the web interface:
  ```bash
  python app.py
  ```
- Access the interface at `http://127.0.0.1:5000`.

## Data Sources

- **Ethiopian Earthquakes Dataset**: Included in `ethiopian_earthquakes.csv`.
- **External Data Sources**: https://earthquake.usgs.gov/fdsnws/event/1/query

## Dependencies

See `requirements.txt` for a list of Python packages required for this project.




