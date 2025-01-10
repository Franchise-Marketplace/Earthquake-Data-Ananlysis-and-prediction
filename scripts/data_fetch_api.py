import requests
import json
import pandas as pd

def fetch_data():
    # Define Ethiopia's bounding box
    ethiopia_bbox = {
        "minlatitude": 3.422,
        "maxlatitude": 14.959,
        "minlongitude": 32.999,
        "maxlongitude": 47.986,
    }

    # Define the time range (past 75 years)
    params = {
        "format": "geojson",
        "starttime": "1950-01-01",
        "endtime": "2025-01-01",
        "minlatitude": ethiopia_bbox["minlatitude"],
        "maxlatitude": ethiopia_bbox["maxlatitude"],
        "minlongitude": ethiopia_bbox["minlongitude"],
        "maxlongitude": ethiopia_bbox["maxlongitude"],
        "minmagnitude": 3.0,  # Filter earthquakes with magnitude >= 3.0
        "orderby": "time",
    }

    # Fetch data from USGS API
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        # Parse earthquake data
        earthquakes = [
            {
                "time": feature["properties"]["time"],
                "latitude": feature["geometry"]["coordinates"][1],
                "longitude": feature["geometry"]["coordinates"][0],
                "depth": feature["geometry"]["coordinates"][2],
                "magnitude": feature["properties"]["mag"],
                "place": feature["properties"]["place"],
            }
            for feature in data["features"]
        ]

        # Convert to DataFrame for better handling
        df = pd.DataFrame(earthquakes)
        print(df.head())

        # Save to CSV
        df.to_csv("../data/raw/ethiopian_earthquakes.csv", index=False)
        print("Data saved to ethiopian_earthquakes.csv")

    else:
        print(f"Error fetching data: {response.status_code}")
