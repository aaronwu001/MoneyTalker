import json
import os

def split_and_store_json(file_name, output_folder, chunk_size=500):
    """
    Reads a JSON file, splits the 'USD' data into chunks, and stores each chunk in separate JSON files.

    Args:
        file_name (str): The name of the JSON file to process.
        output_folder (str): The folder to store the chunked JSON files.
        chunk_size (int): The number of entries per chunk.
    """
    # Check if the file exists
    if not os.path.exists(file_name):
        print(f"File '{file_name}' not found.")
        return

    # Load the file
    with open(file_name, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print("Error: File is not a valid JSON file.")
            return

    # Ensure the file has the expected structure
    if data.get("taxonomy") != "us-gaap" or "units" not in data or "USD" not in data["units"]:
        print(f"File '{file_name}' does not match the expected structure.")
        return

    # Extract the relevant data from 'units' -> 'USD'
    entries = data["units"]["USD"]
    if not entries:
        print(f"No data found in 'units' -> 'USD' for file '{file_name}'.")
        return

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Split data into chunks and save each chunk as a new JSON file
    for idx, chunk_start in enumerate(range(0, len(entries), chunk_size)):
        chunk = entries[chunk_start:chunk_start + chunk_size]
        output_file = os.path.join(output_folder, f"chunk_{idx + 1}.json")
        with open(output_file, "w") as output:
            json.dump(chunk, output, indent=2)
        print(f"Saved chunk {idx + 1} to '{output_file}'.")

# Example usage
if __name__ == "__main__":
    # Input JSON file in the same folder as this script
    file_name = "Revenues.json"  # Replace with your file name

    # Output folder to store the split chunks
    output_folder = "./split_files"  # Replace with your desired output folder

    # Call the function
    split_and_store_json(file_name, output_folder, chunk_size=50)
