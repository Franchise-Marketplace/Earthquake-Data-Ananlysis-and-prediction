import requests
from bs4 import BeautifulSoup
import csv
import os

# Define the URL of the webpage to scrape
url = "https://database.earth/earthquakes/ethiopia"

# Send an HTTP GET request to fetch the webpage content
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to load page {url}, status code: {response.status_code}")

# Parse the webpage content with Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")

# Extract the table rows (adjust the selector based on the page structure)
rows = soup.select("table tbody tr")

# Extract data from the rows
data = []
for row in rows:
    columns = row.find_all("td")
    data.append([col.text.strip() for col in columns])


script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the CSV file
output_path = os.path.join(script_dir, "..\..\data\raw\earthquake_data_scrapped.csv")

# Ensure the parent directory exists
output_dir = os.path.dirname(output_path)
os.makedirs(output_dir, exist_ok=True)

# Save the extracted data to a CSV file
with open(output_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Epicenter", "Magnitude", "Depth"])
    writer.writerows(data)

print(f"Data has been saved to {output_path}")
