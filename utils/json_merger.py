import os
import json
import argparse

def merge_json_files(folder_path, output_file):
    """
    Merges all JSON files in the specified folder into a single JSON file.

    Args:
        folder_path (str): Path to the folder containing JSON files.
        output_file (str): Path to the output JSON file.
    """
    all_data = []

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for record in data:
                        all_data.append(record)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {file_path}: {e}")
            except Exception as e:
                print(f"An error occurred with file {file_path}: {e}")

    # Write the merged data to the output file
    try:
        with open(output_file, 'w') as f:
            json.dump(all_data, f, indent=4)
        print(f"Merged JSON files have been saved to {output_file}")
    except Exception as e:
        print(f"Failed to write to output file {output_file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple JSON files into a single file.")
    parser.add_argument("--folder_path", required=True, help="Path to the folder containing JSON files.")
    parser.add_argument("--output_file", default="merged.json", help="Path for the output JSON file (default: merged.json).")

    args = parser.parse_args()

    merge_json_files(args.folder_path, args.output_file)
