import os
import json

def validate_all_json_files(root_directory="output"):
    """
    Validate all JSON files in the specified root directory and its subdirectories.

    Args:
        root_directory (str): The root directory to search for JSON files.
    """
    print(f"[INFO]: Starting JSON validation in root directory: {root_directory}")
    invalid_files = []  # List to store details of invalid JSON files
    total_files = 0
    valid_files = 0

    # Walk through the root directory and its subdirectories
    for root, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".json"):
                total_files += 1
                file_path = os.path.join(root, file)
                try:
                    # Attempt to load the JSON file
                    with open(file_path, "r", encoding="utf-8") as f:
                        json.load(f)
                    valid_files += 1
                    print(f"[DEBUG]: Successfully validated: {file_path}")
                except json.JSONDecodeError as e:
                    invalid_files.append((file_path, f"JSON Decode Error: {str(e)}"))
                    print(f"[ERROR]: Invalid JSON file: {file_path} - {e}")
                except Exception as e:
                    invalid_files.append((file_path, f"Unexpected Error: {str(e)}"))
                    print(f"[ERROR]: Unexpected error in file: {file_path} - {e}")

    # Print summary
    print("\n[SUMMARY]:")
    print(f"Total JSON files found: {total_files}")
    print(f"Valid JSON files: {valid_files}")
    print(f"Invalid JSON files: {len(invalid_files)}")
    if invalid_files:
        print("\n[INVALID FILES]:")
        for file_path, error in invalid_files:
            print(f" - {file_path}: {error}")

if __name__ == "__main__":
    # The root directory to validate JSON files in
    validate_all_json_files("output")
