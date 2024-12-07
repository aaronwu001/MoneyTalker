import os
import json
import requests
import re

def log_debug(message):
    """Log debug messages for tracing the workflow."""
    print(f"[DEBUG]: {message}")

def sanitize_filename(name):
    """Sanitize filenames to remove invalid characters."""
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def fetch_data(url, headers):
    """Fetch JSON data from a given URL."""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        log_debug(f"Failed to fetch data: {response.status_code} {response.reason}")
        return None

def process_data(data, output_dir):
    """
    Process JSON data to handle all categories, units, and features.
    Args:
        data: The raw JSON data fetched from the API.
        output_dir: Directory where processed files will be stored.
    """
    if not data or 'facts' not in data:
        log_debug("Invalid data structure. No 'facts' key found.")
        return

    entity_name = sanitize_filename(data.get("entityName", "Unknown_Entity"))
    facts = data["facts"]

    # Iterate through categories (e.g., dei, us-gaap)
    for category, features in facts.items():
        log_debug(f"Processing category: {category}")
        category_dir = os.path.join(output_dir, entity_name, sanitize_filename(category))
        os.makedirs(category_dir, exist_ok=True)  # Create category directory

        for feature, feature_data in features.items():
            label = feature_data.get("label", "Unknown_Label")
            description = feature_data.get("description", "No description available.")
            units = feature_data.get("units", {})

            # Process each unit type (e.g., USD, shares)
            for unit, entries in units.items():
                chunk_size = 500  # Define your ideal chunk size
                for i in range(0, len(entries), chunk_size):
                    chunk = entries[i:i + chunk_size]
                    chunk_file = os.path.join(
                        category_dir,
                        f"{sanitize_filename(feature)}_{sanitize_filename(unit)}_chunk{i//chunk_size + 1}.json"
                    )
                    # Include metadata in the chunk
                    chunk_with_metadata = {
                        "entity": entity_name,
                        "category": category,
                        "feature": feature,
                        "unit": unit,
                        "label": label,
                        "description": description,
                        "data": chunk,
                    }
                    with open(chunk_file, "w") as f:
                        json.dump(chunk_with_metadata, f, indent=4)
                    log_debug(f"Saved chunk: {chunk_file}")

def main():
    """Main workflow to fetch, process, and split SEC data."""
    log_debug("Starting SEC data processing workflow...")
    
    cik = "0001318605"  # Example for Tesla
    base_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    headers = {
        "User-Agent": "Your Name (your_email@example.com)",
    }
    output_dir = "./output/tesla_split"
    os.makedirs(output_dir, exist_ok=True)

    # Fetch data from SEC API
    data = fetch_data(base_url, headers)
    if data:
        log_debug("Data fetched successfully.")
        raw_file = os.path.join(output_dir, f"{sanitize_filename(data.get('entityName', 'Unknown'))}_raw.json")
        with open(raw_file, "w") as f:
            json.dump(data, f, indent=4)
        log_debug(f"Raw JSON saved to: {raw_file}")

        # Process and split data
        process_data(data, output_dir)
    else:
        log_debug("No data to process. Exiting.")

    log_debug("Workflow completed.")

if __name__ == "__main__":
    main()
