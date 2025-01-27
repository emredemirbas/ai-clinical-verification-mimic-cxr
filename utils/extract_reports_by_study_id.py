#!/usr/bin/env python3

'''
Use the following command to run this script:
python extract_relevant_reports.py --csv_file mimic-cxr-2.1.0-test-set-labeled.csv --input_folder files --output_file relevant_reports.json
'''


import os
import re
import json
import csv
import argparse
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract relevant radiology reports based on study IDs.")
    parser.add_argument("--csv_file", required=True, help="Path to the CSV file containing study IDs.")
    parser.add_argument("--input_folder", required=True, help="Path to the input folder containing patient subfolders.")
    parser.add_argument("--output_file", required=True, help="Path for the output JSON file.")
    return parser.parse_args()

def load_study_ids(csv_file):
    """
    Load the study IDs from the CSV file.
    """
    study_ids = set()
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            study_ids.add(row['study_id'])
    return study_ids

def extract_findings_and_impression(report_text):
    """
    Extract the 'FINDINGS' and 'IMPRESSION' text blocks from the report.
    """
    report_upper = report_text.upper()
    findings_match = re.search(r'(FINDINGS:)(.*?)(?=IMPRESSION:|$)', report_upper, flags=re.DOTALL)
    impression_match = re.search(r'(IMPRESSION:)(.*)$', report_upper, flags=re.DOTALL)

    findings_text = ""
    impression_text = ""

    if findings_match:
        start_index = report_upper.find(findings_match.group(1))
        end_index = start_index + len(findings_match.group(1) + findings_match.group(2))
        findings_text = report_text[start_index:end_index]
        findings_text = re.sub(r'(?i)^FINDINGS:\s*', '', findings_text.strip())

    if impression_match:
        start_index = report_upper.find(impression_match.group(1))
        end_index = start_index + len(impression_match.group(1) + impression_match.group(2))
        impression_text = report_text[start_index:end_index]
        impression_text = re.sub(r'(?i)^IMPRESSION:\s*', '', impression_text.strip())

    combined = findings_text.strip() + "\n" + impression_text.strip()
    return combined.strip()

def main():
    args = parse_arguments()

    csv_file = args.csv_file
    input_folder = args.input_folder
    output_file = args.output_file

    # Load the study IDs from the CSV file
    study_ids = load_study_ids(csv_file)

    # List to hold all extracted data
    all_reports_data = []

    # Collect all .txt files of interest
    file_paths = []
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith(".txt"):
                # Confirm the parent folder matches pattern "p<number>"
                # and filename matches pattern "s<number>.txt"
                base_folder_name = os.path.basename(root)  # e.g., "p10002428"
                if (re.match(r'^p\d+$', base_folder_name) and
                    re.match(r'^s\d+\.txt$', filename.lower())):
                    file_paths.append(os.path.join(root, filename))

    # Use a progress bar over the collected file paths
    for file_path in tqdm(file_paths, desc="Processing reports"):
        # Parse out patient_id and study_id from folder and file names
        folder_name = os.path.basename(os.path.dirname(file_path))  # e.g., p10002428
        file_name = os.path.basename(file_path)                     # e.g., s58838312.txt

        patient_id = folder_name  # Keep the full folder name (e.g., p10002428)
        study_id = file_name[1:file_name.lower().find('.txt')]  # Remove leading 's' and trailing '.txt'

        # Check if the study_id is in the list of relevant IDs
        if study_id in study_ids:
            # Read the .txt file content
            with open(file_path, 'r', encoding='utf-8') as f:
                report_text = f.read()

            # Extract the FINDINGS and IMPRESSION text
            content = extract_findings_and_impression(report_text)

            # Create an entry for JSON
            entry = {
                "patient_id": patient_id,  # Keep the original format (e.g., p10002428)
                "study_id": f"s{study_id}",  # Add 's' back to the study_id
                "content": content
            }
            all_reports_data.append(entry)

    # Write out to JSON file
    with open(output_file, 'w', encoding='utf-8') as out_f:
        json.dump(all_reports_data, out_f, indent=4, ensure_ascii=False)

    print(f"Extraction completed. {len(all_reports_data)} reports saved to {output_file}.")

if __name__ == "__main__":
    main()