import os
import requests
import json

# Define constants
TESLA_CIK = "0001318605"
BASE_URL = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{TESLA_CIK}.json"
OUTPUT_FOLDER = "processed_data"
HEADERS = {
    "User-Agent": "YourName (your_email@example.com)"  # Replace with your name and email
}

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def fetch_data(url):
    """
    Fetch data from the SEC API.
    """
    try:
        print("Fetching data from the SEC API...")
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise HTTP errors if any
        print("Data fetched successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the data: {e}")
        return None

def split_and_store_data(data, output_folder):
    """
    Split the JSON data by financial concepts and save them into separate files.
    """
    if not data:
        print("No data to process.")
        return

    facts = data.get("facts", {})
    organized_data = {}

    # Organize by taxonomy (e.g., us-gaap, ifrs-full)
    for taxonomy, concepts in facts.items():
        for concept, details in concepts.items():
            # Create a key for each financial concept
            organized_data[concept] = {
                "taxonomy": taxonomy,
                "units": details.get("units", {})
            }

    # Save each concept into a separate file
    for concept, details in organized_data.items():
        file_name = f"{concept}.json"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, "w") as file:
            json.dump(details, file, indent=4)

    print(f"Data split and saved in the '{output_folder}' folder.")

def main():
    # Step 1: Fetch the data
    data = fetch_data(BASE_URL)

    # Step 2: Split and store the data
    split_and_store_data(data, OUTPUT_FOLDER)

if __name__ == "__main__":
    main()
